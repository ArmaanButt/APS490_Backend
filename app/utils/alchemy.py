import uuid


from sqlalchemy.types import (
    TypeDecorator,
    VARBINARY,
)


class UnboundTypeDecorator(TypeDecorator):

    def result_processor(self, dialect, coltype):
        return lambda value: self.process_result_value(value, dialect)

    def bind_processor(self, dialect):
        """ Simple override to avoid pre-processing before
        process_bind_param. This is for when the Python type can't
        be easily coerced into the `impl` type."""
        return lambda value: self.process_bind_param(value, dialect)


class UUID(UnboundTypeDecorator):
    """ A memory-efficient MySQL UUID-type. """

    impl = VARBINARY(16)

    def process_bind_param(self, value, dialect):
        """ Emit the param in hex notation. """
        value = uuid.UUID(str(value))
        return value if value is None else value.bytes

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            assert len(value) == 16, "Expected 16 bytes, got %d" % len(value)
            return uuid.UUID(bytes=value)
