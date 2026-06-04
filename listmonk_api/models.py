from pydantic import AliasChoices, BaseModel, Field
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
    # Issue #3: listmonk's create-campaign payload key is "type" (older wrappers
    # used "send_type"). Accept either on input (legacy "send_type" or "type"),
    # but always serialize to "type" so model_dump(by_alias=True) sends the key
    # listmonk expects.
    type: str = Field(
        validation_alias=AliasChoices("send_type", "type"),
        serialization_alias="type",
    )
    content_type: str
    body: str
    altbody: Optional[str] = None
    send_at: Optional[str] = None
    messenger: Optional[str] = None
    template_id: Optional[int] = None
    tags: Optional[List[str]] = None
    # Issue #4: attach uploaded media to a campaign. Listmonk campaigns reference
    # attachments by media ID (upload first via the Media API), serialized as the
    # "media" key, e.g. {"media": [1, 2]}. (Base64/file attachments are a
    # transactional-message feature — see TransactionalMessageRequest.)
    media: Optional[List[int]] = None


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
