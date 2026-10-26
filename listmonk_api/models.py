from typing import Any

from pydantic import AliasChoices, BaseModel, Field


class SubscriberCreateRequest(BaseModel):
    email: str
    name: str
    status: str
    lists: list[int] | None = None
    attribs: dict[str, Any] | None = None
    preconfirm_subscriptions: bool | None = True


class ListCreateRequest(BaseModel):
    name: str
    type: str  # visibility_type: 'public' or 'private'
    optin: str  # 'single' or 'double'
    tags: list[str] | None = None


class ListEditRequest(BaseModel):
    name: str | None = None
    type: str | None = None
    optin: str | None = None
    tags: list[str] | None = None


class ImportSubscribersRequest(BaseModel):
    file: str  # Base64 encoded or content depending on Listmonk API docs, wait, Listmonk expects binary upload or text? The wrapper takes 'file' as text or base64. Wait, the old wrapper did json dump with `file`... wait, it actually just sent `{"file": "..."}`.
    mode: str
    delim: str = ","
    lists: list[int]
    overwrite: bool = True


class CampaignCreateRequest(BaseModel):
    name: str
    subject: str
    lists: list[int]
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
    altbody: str | None = None
    send_at: str | None = None
    messenger: str | None = None
    template_id: int | None = None
    tags: list[str] | None = None
    # Issue #4: attach uploaded media to a campaign. Listmonk campaigns reference
    # attachments by media ID (upload first via the Media API), serialized as the
    # "media" key, e.g. {"media": [1, 2]}. (Base64/file attachments are a
    # transactional-message feature — see TransactionalMessageRequest.)
    media: list[int] | None = None


class CampaignStatusRequest(BaseModel):
    status: str  # 'scheduled', 'running', 'paused', 'cancelled'


class MediaUploadRequest(BaseModel):
    file: str


class TemplateDefaultRequest(BaseModel):
    pass  # No body required, just the path param


class TransactionalMessageRequest(BaseModel):
    template_id: int
    subscriber_email: str | None = None
    subscriber_id: int | None = None
    data: dict[str, Any] | None = None
    headers: list[dict[str, str]] | None = None
    content_type: str | None = None
    # Fix: Added attachment support
    attachments: list[dict[str, str]] | None = None
