from typing import Any, List, Optional

from app.core.logger import logger
from app.api.api_schemas import ErrorSchema
from app.api.exceptions import NotFoundException

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder


def error_response(
    message: str,
    details: Optional[List[Any]] = None,
    status_code: int = 500
) -> JSONResponse:
    """Generate a standardized JSON error response.

    Args:
        message (str): A human-readable error message.
        details (Optional[List[Any]]): Additional technical or contextual information. Defaults to None.
        status_code (int): HTTP status code to return. Defaults to 500.

    Returns:
        JSONResponse: A FastAPI JSONResponse containing the structured error payload.
    """
    logger.error('Error occurred: %s | Details: %s | Status code: %d', message, details, status_code)
    schema = ErrorSchema(message=message, details=details)
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(schema)
    )


def register_exception_handlers(exception_handler: FastAPI):
    """Register global exception handlers for the FastAPI application.

    This function sets up handlers for common exceptions such as validation errors,
    HTTP exceptions, SQLAlchemy integrity errors, and uncaught generic exceptions.
    All exceptions will return standardized JSON responses according to the ErrorSchema.

    Args:
        app (FastAPI): The FastAPI application instance on which to register the handlers.

    Returns:
        None: This function does not return anything. It modifies the app in-place.
    """

    @exception_handler.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError): # type: ignore
        """Handle Pydantic request validation errors (HTTP 422).

        This handler catches validation errors raised by FastAPI/Pydantic when the request
        body, query parameters, or path parameters do not conform to the expected schema.
        It returns a standardized JSON response according to the ErrorSchema.

        Args:
            request (Request): The FastAPI request object that caused the validation error.
            exc (RequestValidationError): The exception instance containing validation error details.

        Returns:
            JSONResponse: A standardized JSON response with HTTP status 422 and a list
                        of validation errors.
        """
        errors: List[dict] = [dict(e) for e in exc.errors()] # type: ignore
        logger.warning(
            'Validation error on request %s %s | Details: %s',
            request.method,
            request.url.path,
            errors # type: ignore
        )
        return error_response(
            message="Validation error",
            details=errors, # type: ignore
            status_code=422
        )

    @exception_handler.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError): # type: ignore
        """Handle SQLAlchemy integrity constraint violations (HTTP 400).

        This handler catches database errors raised by SQLAlchemy when an operation
        violates a database constraint, such as unique constraints, foreign keys, 
        or not-null constraints. It returns a standardized JSON response according to 
        the ErrorSchema.

        Args:
            request (Request): The FastAPI request object that caused the database error.
            exc (IntegrityError): The exception instance containing details about the
                                database integrity violation.

        Returns:
            JSONResponse: A standardized JSON response with HTTP status 400 and
                        details about the database constraint violation.
        """
        errors = [{"error": str(exc.orig)}]

        logger.error(
            'Database integrity error on request %s %s | Details: %s',
            request.method,
            request.url.path,
            errors,
            exc_info=exc  # type: ignore
        )

        return error_response(
            message="Database integrity error",
            details=errors,
            status_code=400
        )

    @exception_handler.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException): # type: ignore
        """Handle generic HTTP exceptions raised by FastAPI.

        This handler catches HTTP exceptions such as 404 Not Found, 403 Forbidden, 
        and 401 Unauthorized, and returns a standardized JSON response according 
        to the ErrorSchema.

        Args:
            request (Request): The FastAPI request object that caused the HTTP exception.
            exc (HTTPException): The HTTPException instance with status code and detail message.

        Returns:
            JSONResponse: A standardized JSON response with the HTTP status code and 
                        the exception message.
        """
        if 400 <= exc.status_code < 500:
            logger.warning(
                'HTTP exception on request %s %s | Status: %d | Detail: %s',
                request.method,
                request.url.path,
                exc.status_code,
                exc.detail
            )
        else:
            logger.error(
                'HTTP exception on request %s %s | Status: %d | Detail: %s',
                request.method,
                request.url.path,
                exc.status_code,
                exc.detail
            )
        
        return error_response(
            message=str(exc.detail),
            details=None,
            status_code=exc.status_code
        )

    @exception_handler.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception): # type: ignore
        """Handle all uncaught exceptions in the application.

        This handler serves as a catch-all for any exceptions that are not 
        specifically handled by other exception handlers. It returns a standardized 
        JSON response according to the ErrorSchema, ensuring consistent error 
        responses across the API.

        Args:
            request (Request): The FastAPI request object that caused the exception.
            exc (Exception): The uncaught exception instance.

        Returns:
            JSONResponse: A standardized JSON response with status code 500 and 
                        the exception details.
        """
        errors = [{"error": str(exc)}]
    
        logger.error(
            'Unhandled exception on request %s %s | Details: %s',
            request.method,
            request.url.path,
            errors,
            exc_info=exc
        )
        
        return error_response(
            message="Internal server error",
            details=errors,
            status_code=500
        )
    
    @exception_handler.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):  # type: ignore
        """Handle cases where a requested resource is not found (HTTP 404).

        This handler catches `NotFoundException` exceptions raised by the application
        when a requested entity (e.g., user, enterprise, product) does not exist in
        the database. It returns a standardized JSON response following the
        ErrorSchema structure.

        Args:
            request (Request): The FastAPI request object that caused the exception.
            exc (NotFoundException): The exception instance containing information
                about the missing resource.

        Returns:
            JSONResponse: A structured JSON error response with status code 404 and
                details about the missing resource.
        """
        errors = [{"resource": exc.resource, "id": exc.resource_id}]  # type: ignore

        logger.warning(
            'Resource not found on request %s %s | Details: %s',
            request.method,
            request.url.path,
            errors # type: ignore
        )
        
        return error_response(
            message=exc.message,
            details=errors,  # type: ignore
            status_code=404
        )