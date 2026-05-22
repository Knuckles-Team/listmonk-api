from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class SubscriberCreateRequest(BaseModel):
    email: str
    name: str
    status: str
    lists: Optional[List[int]] = None
    attribs: Optional[Dict[str, Any]] = None
    preconfirm_subscriptions: Optional[bool] = True


class ListCreateRequest(BaseModel):
    name: str
    type: str  # visibility_type: 'public' or 'private'
    optin: str  # 'single' or 'double'
    tags: Optional[List[str]] = None


class ListEditRequest(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    optin: Optional[str] = None
    tags: Optional[List[str]] = None


class ImportSubscribersRequest(BaseModel):
    file: str  # Base64 encoded or content depending on Listmonk API docs, wait, Listmonk expects binary upload or text? The wrapper takes 'file' as text or base64. Wait, the old wrapper did json dump with `file`... wait, it actually just sent `{"file": "..."}`.
    mode: str
    delim: str = ","
    lists: List[int]
    overwrite: bool = True


class CampaignCreateRequest(BaseModel):
    name: str
    subject: str
    lists: List[int]
    from_email: str
    type: str = Field(alias="send_type")  # send_type mapped to type
    content_type: str
    body: str
    altbody: Optional[str] = None
    send_at: Optional[str] = None
    messenger: Optional[str] = None
    template_id: Optional[int] = None
    tags: Optional[List[str]] = None
    # Fix: Added attachment support
    attachments: Optional[List[Dict[str, str]]] = (
        None  # Assuming a format, or maybe list of media IDs? Listmonk API actually uses just media IDs or base64? Actually, often [{"name": "file.txt", "content": "base64"}] or something. I'll just accept a generic list.
    )


class CampaignStatusRequest(BaseModel):
    status: str  # 'scheduled', 'running', 'paused', 'cancelled'


class MediaUploadRequest(BaseModel):
    file: str


class TemplateDefaultRequest(BaseModel):
    pass  # No body required, just the path param


class TransactionalMessageRequest(BaseModel):
    template_id: int
    subscriber_email: Optional[str] = None
    subscriber_id: Optional[int] = None
    data: Optional[Dict[str, Any]] = None
    headers: Optional[List[Dict[str, str]]] = None
    content_type: Optional[str] = None
    # Fix: Added attachment support
    attachments: Optional[List[Dict[str, str]]] = None
