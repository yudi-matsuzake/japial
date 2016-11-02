# -*- coding: utf-8 -*-

class ErrorCode(Exception):
    """Describes the http errors"""
    def __init__(self, code, msg, category=None, description=None):
        super(ErrorCode, self).__init__(msg)
        self.code        = code
        self.msg         = msg
        self.category    = category
        self.description = description

http_continue = ErrorCode(
          code        = 0,
          msg         = 'Continue',
          category    = 'Information',
          description = 'The server has received the request headers, and the client should proceed to send the request body')

switching_protocols = ErrorCode(
          code        = 1,
          msg         = 'Switching Protocols',
          category    = 'Information',
          description = 'The requester has asked the server to switch protocols')

checkpoint = ErrorCode(
          code        = 3,
          msg         = 'Checkpoint',
          category    = 'Information',
          description = 'Used in the resumable requests proposal to resume aborted PUT or POST requests')

ok = ErrorCode(
          code        = 200,
          msg         = 'OK',
          category    = 'Successful',
          description = 'The request is OK')

created = ErrorCode(
          code        = 201,
          msg         = 'Created',
          category    = 'Successful',
          description = 'The request has been fulfilled, and a new resource is created')

accepted = ErrorCode(
          code        = 202,
          msg         = 'Accepted',
          category    = 'Successful',
          description = 'The request has been accepted for processing, but the processing has not been completed')

non_authoritative_information = ErrorCode(
          code        = 203,
          msg         = 'Non-Authoritative Information',
          category    = 'Successful',
          description = 'The request has been successfully processed, but is returning information that may be from another source')

no_content = ErrorCode(
          code        = 204,
          msg         = 'No Content',
          category    = 'Successful',
          description = 'The request has been successfully processed, but is not returning any content')

reset_content = ErrorCode(
          code        = 205,
          msg         = 'Reset Content',
          category    = 'Successful',
          description = 'The request has been successfully processed, but is not returning any content, and requires that the requester reset the document view')

partial_content = ErrorCode(
          code        = 206,
          msg         = 'Partial Content',
          category    = 'Successful',
          description = 'The server is delivering only part of the resource due to a range header sent by the client')

multiple_choices = ErrorCode(
          code        = 300,
          msg         = 'Multiple Choices',
          category    = 'Redirection',
          description = 'A link list. The user can select a link and go to that location. Maximum five addresses')

moved_permanently = ErrorCode(
          code        = 301,
          msg         = 'Moved Permanently',
          category    = 'Redirection',
          description = 'The requested page has moved to a new URL')

found = ErrorCode(
          code        = 302,
          msg         = 'Found',
          category    = 'Redirection',
          description = 'The requested page has moved temporarily to a new URL')

see_other = ErrorCode(
          code        = 303,
          msg         = 'See Other',
          category    = 'Redirection',
          description = 'The requested page can be found under a different URL')

not_modified = ErrorCode(
          code        = 304,
          msg         = 'Not Modified',
          category    = 'Redirection',
          description = 'Indicates the requested page has not been modified since last requested')

switch_proxy = ErrorCode(
          code        = 306,
          msg         = 'Switch Proxy',
          category    = 'Redirection',
          description = 'No longer used')

temporary_redirect = ErrorCode(
          code        = 307,
          msg         = 'Temporary Redirect',
          category    = 'Redirection',
          description = 'The requested page has moved temporarily to a new URL')

resume_incomplete = ErrorCode(
          code        = 308,
          msg         = 'Resume Incomplete',
          category    = 'Redirection',
          description = 'Used in the resumable requests proposal to resume aborted PUT or POST requests')

bad_request = ErrorCode(
          code        = 400,
          msg         = 'Bad Request',
          category    = 'Client Error',
          description = 'The request cannot be fulfilled due to bad syntax')

unauthorized = ErrorCode(
          code        = 401,
          msg         = 'Unauthorized',
          category    = 'Client Error',
          description = 'The request was a legal request, but the server is refusing to respond to it. For use when authentication is possible but has failed or not yet been provided')

payment_required = ErrorCode(
          code        = 402,
          msg         = 'Payment Required',
          category    = 'Client Error',
          description = 'Reserved for future use')

forbidden = ErrorCode(
          code        = 403,
          msg         = 'Forbidden',
          category    = 'Client Error',
          description = 'The request was a legal request, but the server is refusing to respond to it')

not_found = ErrorCode(
          code        = 404,
          msg         = 'Not Found',
          category    = 'Client Error',
          description = 'The requested page could not be found but may be available again in the future')

method_not_allowed = ErrorCode(
          code        = 405,
          msg         = 'Method Not Allowed',
          category    = 'Client Error',
          description = 'A request was made of a page using a request method not supported by that page')

not_acceptable = ErrorCode(
          code        = 406,
          msg         = 'Not Acceptable',
          category    = 'Client Error',
          description = 'The server can only generate a response that is not accepted by the client')

proxy_authentication_required = ErrorCode(
          code        = 407,
          msg         = 'Proxy Authentication Required',
          category    = 'Client Error',
          description = 'The client must first authenticate itself with the proxy')

request_timeout = ErrorCode(
          code        = 408,
          msg         = 'Request Timeout',
          category    = 'Client Error',
          description = 'The server timed out waiting for the request')

conflict = ErrorCode(
          code        = 409,
          msg         = 'Conflict',
          category    = 'Client Error',
          description = 'The request could not be completed because of a conflict in the request')

gone = ErrorCode(
          code        = 410,
          msg         = 'Gone',
          category    = 'Client Error',
          description = 'The requested page is no longer available')

length_required = ErrorCode(
          code        = 411,
          msg         = 'Length Required',
          category    = 'Client Error',
          description = 'The "Content-Length" is not defined. The server will not accept the request without it')

precondition_failed = ErrorCode(
          code        = 412,
          msg         = 'Precondition Failed',
          category    = 'Client Error',
          description = 'The precondition given in the request evaluated to false by the server')

request_entity_too_large = ErrorCode(
          code        = 413,
          msg         = 'Request Entity Too Large',
          category    = 'Client Error',
          description = 'The server will not accept the request, because the request entity is too large')

request_uri_too_long = ErrorCode(
          code        = 414,
          msg         = 'Request-URI Too Long',
          category    = 'Client Error',
          description = 'The server will not accept the request, because the URL is too long. Occurs when you convert a POST request to a GET request with a long query information')

unsupported_media_type = ErrorCode(
          code        = 415,
          msg         = 'Unsupported Media Type',
          category    = 'Client Error',
          description = 'The server will not accept the request, because the media type is not supported')

requested_range_not_satisfiable = ErrorCode(
          code        = 416,
          msg         = 'Requested Range Not Satisfiable',
          category    = 'Client Error',
          description = 'The client has asked for a portion of the file, but the server cannot supply that portion')

expectation_failed = ErrorCode(
          code        = 417,
          msg         = 'Expectation Failed',
          category    = 'Client Error',
          description = 'The server cannot meet the requirements of the Expect request-header field')

internal_server_error = ErrorCode(
          code        = 500,
          msg         = 'Internal Server Error',
          category    = 'Server Error',
          description = 'A generic error message, given when no more specific message is suitable')

not_implemented = ErrorCode(
          code        = 501,
          msg         = 'Not Implemented',
          category    = 'Server Error',
          description = 'The server either does not recognize the request method, or it lacks the ability to fulfill the request')

bad_gateway = ErrorCode(
          code        = 502,
          msg         = 'Bad Gateway',
          category    = 'Server Error',
          description = 'The server was acting as a gateway or proxy and received an invalid response from the upstream server')

service_unavailable = ErrorCode(
          code        = 503,
          msg         = 'Service Unavailable',
          category    = 'Server Error',
          description = 'The server is currently unavailable (overloaded or down)')

gateway_timeout = ErrorCode(
          code        = 504,
          msg         = 'Gateway Timeout',
          category    = 'Server Error',
          description = 'The server was acting as a gateway or proxy and did not receive a timely response from the upstream server')

http_version_not_supported = ErrorCode(
          code        = 505,
          msg         = 'HTTP Version Not Supported',
          category    = 'Server Error',
          description = 'The server does not support the HTTP protocol version used in the request')

network_authentication_required = ErrorCode(
          code        = 511,
          msg         = 'Network Authentication Required',
          category    = 'Server Error',
          description = 'The client needs to authenticate to gain network access')

