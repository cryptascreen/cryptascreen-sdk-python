"""Models of the CryptaScreen API (generated from the @cryptascreen/sdk 0.2.2 types)."""

from __future__ import annotations

from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class CsModel(BaseModel):
    """Base model: wire names are camelCase, unknown fields are kept (forward compatible)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class PaginatedResponse(CsModel, Generic[T]):
    """Generic page: ``data`` + paging counters."""

    data: list[T] = Field(default_factory=list)
    page: int = 0
    page_size: int = Field(default=0, alias="pageSize")
    total_items: int = Field(default=0, alias="totalItems")
    total_pages: int = Field(default=0, alias="totalPages")


class CaseStatus(str, Enum):
    """Known values of CaseStatus."""

    OPEN = "OPEN"
    IN_REVIEW = "IN_REVIEW"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class CasePriority(str, Enum):
    """Known values of CasePriority."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class GraphScopeStatus(str, Enum):
    """Known values of GraphScopeStatus."""

    COMPLETE = "COMPLETE"
    TRUNCATED = "TRUNCATED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_EXPANDED = "NOT_EXPANDED"


class GraphStatus(str, Enum):
    """Known values of GraphStatus."""

    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    TRUNCATED = "TRUNCATED"
    FAILED = "FAILED"
    UNSUPPORTED = "UNSUPPORTED"
    UNAVAILABLE = "UNAVAILABLE"


class GraphExportFormat(str, Enum):
    """Known values of GraphExportFormat."""

    JSON = "json"
    CSV = "csv"


class NameSubjectType(str, Enum):
    """Known values of NameSubjectType."""

    PERSON = "PERSON"
    ENTITY = "ENTITY"
    VESSEL = "VESSEL"
    AIRCRAFT = "AIRCRAFT"


class NameIdentifierType(str, Enum):
    """Known values of NameIdentifierType."""

    PASSPORT = "PASSPORT"
    NATIONAL_ID = "NATIONAL_ID"
    TAX_ID = "TAX_ID"
    REGISTRATION_NUMBER = "REGISTRATION_NUMBER"
    LEI = "LEI"
    IMO = "IMO"
    OTHER = "OTHER"


class NameOutcome(str, Enum):
    """Known values of NameOutcome."""

    CLEAR = "CLEAR"
    REVIEW = "REVIEW"
    CONFIRMED_MATCH = "CONFIRMED_MATCH"


class NameMatchStrength(str, Enum):
    """Known values of NameMatchStrength."""

    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    STRICT = "STRICT"


class NameReasonOutcome(str, Enum):
    """Known values of NameReasonOutcome."""

    MATCH = "MATCH"
    PARTIAL = "PARTIAL"
    CONTRADICTS = "CONTRADICTS"
    ABSENT = "ABSENT"


class RiskLevel(str, Enum):
    """Known values of RiskLevel."""

    MINIMAL = "MINIMAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class Coverage(str, Enum):
    """Known values of Coverage."""

    COVERED = "COVERED"
    NOT_ANALYZED = "NOT_ANALYZED"


class HeuristicsStatus(str, Enum):
    """Known values of HeuristicsStatus."""

    UNAVAILABLE = "UNAVAILABLE"
    SKIPPED = "SKIPPED"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    UNSUPPORTED = "UNSUPPORTED"
    QUOTA_REACHED = "QUOTA_REACHED"
    NOT_INCLUDED_IN_PLAN = "NOT_INCLUDED_IN_PLAN"


class DetectorOutcome(str, Enum):
    """Known values of DetectorOutcome."""

    RAN = "RAN"
    TRUNCATED = "TRUNCATED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    SKIPPED_UNSUPPORTED = "SKIPPED_UNSUPPORTED"
    DISABLED = "DISABLED"


class LayerState(str, Enum):
    """Known values of LayerState."""

    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"
    FAILED = "FAILED"
    NOT_REQUESTED = "NOT_REQUESTED"
    NOT_ENTITLED = "NOT_ENTITLED"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    PENDING = "PENDING"


class AssessmentStatus(str, Enum):
    """Known values of AssessmentStatus."""

    COMPLETE = "COMPLETE"
    CHECKED_LAYERS_ONLY = "CHECKED_LAYERS_ONLY"
    INCOMPLETE = "INCOMPLETE"
    NOT_ANALYZED = "NOT_ANALYZED"


class Disposition(str, Enum):
    """Known values of Disposition."""

    BLOCKING_MATCH = "BLOCKING_MATCH"
    RESTRICTION_MATCH = "RESTRICTION_MATCH"
    CANDIDATE_REVIEW = "CANDIDATE_REVIEW"
    RISK_INDICATORS = "RISK_INDICATORS"
    CONTEXT_ONLY = "CONTEXT_ONLY"
    NO_MATCH_IN_CHECKED_LAYERS = "NO_MATCH_IN_CHECKED_LAYERS"


class MatchState(str, Enum):
    """Known values of MatchState."""

    CONFIRMED = "CONFIRMED"
    CANDIDATE = "CANDIDATE"
    CONTEXT = "CONTEXT"
    EXPIRED = "EXPIRED"
    DISPUTED = "DISPUTED"


class FindingCategory(str, Enum):
    """Known values of FindingCategory."""

    SANCTIONS = "SANCTIONS"
    THREAT_INTEL = "THREAT_INTEL"
    PEP = "PEP"
    ENTITY_LABEL = "ENTITY_LABEL"
    ON_CHAIN = "ON_CHAIN"


class VendorLayerStatus(str, Enum):
    """Known values of VendorLayerStatus."""

    OK = "OK"
    TIMEOUT = "TIMEOUT"
    SKIPPED_CAP = "SKIPPED_CAP"
    SKIPPED_BREAKER = "SKIPPED_BREAKER"
    AUTH_FAILED = "AUTH_FAILED"
    RATE_LIMITED = "RATE_LIMITED"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_FOUND = "NOT_FOUND"
    UNSUPPORTED_CHAIN = "UNSUPPORTED_CHAIN"
    UNEXPECTED_RESPONSE = "UNEXPECTED_RESPONSE"


class CacheDecision(str, Enum):
    """Known values of CacheDecision."""

    HIT = "HIT"
    MISS = "MISS"
    FORCE_REFRESH = "FORCE_REFRESH"
    FINDINGS_PRESENT = "FINDINGS_PRESENT"
    STALE_VERSION = "STALE_VERSION"
    SCOPE_MISMATCH = "SCOPE_MISMATCH"
    SAFETY_TTL_EXPIRED = "SAFETY_TTL_EXPIRED"
    NOT_REUSABLE = "NOT_REUSABLE"
    VERSION_UNKNOWN = "VERSION_UNKNOWN"


class ScreeningJobStatus(str, Enum):
    """Known values of ScreeningJobStatus."""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WalletSectionState(str, Enum):
    """Known values of WalletSectionState."""

    COMPLETE = "COMPLETE"
    TRUNCATED = "TRUNCATED"
    PARTIAL = "PARTIAL"
    NOT_ANALYZED = "NOT_ANALYZED"


class WalletTransferCountBasis(str, Enum):
    """Known values of WalletTransferCountBasis."""

    EXACT = "EXACT"
    AT_LEAST = "AT_LEAST"
    UPPER_BOUND = "UPPER_BOUND"
    UNKNOWN = "UNKNOWN"


class WalletExposureCategory(str, Enum):
    """Known values of WalletExposureCategory."""

    SANCTIONS = "SANCTIONS"
    STATE_LINKED_THEFT = "STATE_LINKED_THEFT"
    HACK = "HACK"
    SCAM = "SCAM"
    RANSOMWARE = "RANSOMWARE"
    SANCTIONS_EVASION = "SANCTIONS_EVASION"
    ISSUER_FROZEN = "ISSUER_FROZEN"
    OTHER_LISTED = "OTHER_LISTED"


class WebhookEventType(str, Enum):
    """Known values of WebhookEventType."""

    HIGH_RISK = "HIGH_RISK"
    CRITICAL = "CRITICAL"
    SANCTIONS_MATCH = "SANCTIONS_MATCH"
    HEURISTICS_COMPLETE = "HEURISTICS_COMPLETE"
    TEST = "TEST"


class InvestigationCase(CsModel):
    """InvestigationCase (see types/cases.ts in @cryptascreen/sdk)."""

    id: str | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_id: str | None = Field(default=None, alias="assigneeId")
    addresses: list[Any] | None = None
    notes: list[CaseNote] | None = None
    evidence: list[CaseEvidence] | None = None
    events: list[CaseEvent] | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    updated_at: str | None = Field(default=None, alias="updatedAt")
    resolved_at: str | None = Field(default=None, alias="resolvedAt")


class CaseNote(CsModel):
    """CaseNote (see types/cases.ts in @cryptascreen/sdk)."""

    id: str | None = None
    case_id: str | None = Field(default=None, alias="caseId")
    author_id: str | None = Field(default=None, alias="authorId")
    content: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")


class CaseEvidence(CsModel):
    """CaseEvidence (see types/cases.ts in @cryptascreen/sdk)."""

    id: str | None = None
    case_id: str | None = Field(default=None, alias="caseId")
    type: str | None = None
    label: str | None = None
    url: str | None = None
    metadata: dict[str, Any] | None = None
    added_at: str | None = Field(default=None, alias="addedAt")
    added_by: str | None = Field(default=None, alias="addedBy")


class CaseEvent(CsModel):
    """CaseEvent (see types/cases.ts in @cryptascreen/sdk)."""

    id: str | None = None
    case_id: str | None = Field(default=None, alias="caseId")
    event_type: str | None = Field(default=None, alias="eventType")
    description: str | None = None
    actor_id: str | None = Field(default=None, alias="actorId")
    metadata: dict[str, Any] | None = None
    occurred_at: str | None = Field(default=None, alias="occurredAt")


class CreateCaseRequest(CsModel):
    """CreateCaseRequest (see types/cases.ts in @cryptascreen/sdk)."""

    title: str
    description: str | None = None
    priority: str | None = None
    assignee_id: str | None = Field(default=None, alias="assigneeId")
    addresses: list[Any]


class UpdateCaseStatusRequest(CsModel):
    """UpdateCaseStatusRequest (see types/cases.ts in @cryptascreen/sdk)."""

    status: str
    reason: str | None = None


class AddNoteRequest(CsModel):
    """AddNoteRequest (see types/cases.ts in @cryptascreen/sdk)."""

    content: str


class AddEvidenceRequest(CsModel):
    """AddEvidenceRequest (see types/cases.ts in @cryptascreen/sdk)."""

    type: str
    label: str
    url: str | None = None
    metadata: dict[str, Any] | None = None


class EscalateCaseRequest(CsModel):
    """EscalateCaseRequest (see types/cases.ts in @cryptascreen/sdk)."""

    reason: str
    assignee_id: str | None = Field(default=None, alias="assigneeId")


class ListCasesParams(CsModel):
    """ListCasesParams (see types/cases.ts in @cryptascreen/sdk)."""

    status: str | None = None
    priority: str | None = None
    page: int | None = None
    page_size: int | None = Field(default=None, alias="pageSize")


class CryptaScreenConfig(CsModel):
    """CryptaScreenConfig (see types/common.ts in @cryptascreen/sdk)."""

    base_url: str | None = Field(default=None, alias="baseUrl")
    api_key: str | None = Field(default=None, alias="apiKey")
    timeout: float | None = None
    retries: float | None = None


class PaginationParams(CsModel):
    """PaginationParams (see types/common.ts in @cryptascreen/sdk)."""

    page: int | None = None
    page_size: int | None = Field(default=None, alias="pageSize")


class ApiError(CsModel):
    """ApiError (see types/common.ts in @cryptascreen/sdk)."""

    status: float | None = None
    code: str | None = None
    message: str | None = None
    details: dict[str, Any] | None = None
    request_id: str | None = Field(default=None, alias="requestId")


class ApiResponse(CsModel):
    """ApiResponse (see types/common.ts in @cryptascreen/sdk)."""

    data: Any = None
    request_id: str | None = Field(default=None, alias="requestId")


class TravelRuleCheckRequest(CsModel):
    """TravelRuleCheckRequest (see types/compliance.ts in @cryptascreen/sdk)."""

    tx_hash: str | None = Field(default=None, alias="txHash")
    chain: str
    from_address: str = Field(alias="fromAddress")
    to_address: str = Field(alias="toAddress")
    transfer_amount_usd: float = Field(alias="transferAmountUsd")


class TravelRuleCheckResult(CsModel):
    """TravelRuleCheckResult (see types/compliance.ts in @cryptascreen/sdk)."""

    tx_hash: str | None = Field(default=None, alias="txHash")
    chain: str | None = None
    required: bool | None = None
    threshold_exceeded: bool | None = Field(default=None, alias="thresholdExceeded")
    threshold_usd: float | None = Field(default=None, alias="thresholdUsd")
    originator_vasp_identified: bool | None = Field(default=None, alias="originatorVaspIdentified")
    originator_vasp_name: str | None = Field(default=None, alias="originatorVaspName")
    beneficiary_vasp_identified: bool | None = Field(
        default=None, alias="beneficiaryVaspIdentified"
    )
    beneficiary_vasp_name: str | None = Field(default=None, alias="beneficiaryVaspName")
    travel_rule_protocol: str | None = Field(default=None, alias="travelRuleProtocol")


class TravelRulePayloadRequest(CsModel):
    """TravelRulePayloadRequest (see types/compliance.ts in @cryptascreen/sdk)."""

    tx_hash: str | None = Field(default=None, alias="txHash")
    chain: str
    originator_name: str | None = Field(default=None, alias="originatorName")
    originator_first_name: str | None = Field(default=None, alias="originatorFirstName")
    originator_last_name: str | None = Field(default=None, alias="originatorLastName")
    originator_wallet_address: str = Field(alias="originatorWalletAddress")
    originator_vasp_name: str | None = Field(default=None, alias="originatorVaspName")
    transfer_amount_usd: float = Field(alias="transferAmountUsd")


class TravelRulePayload(CsModel):
    """TravelRulePayload (see types/compliance.ts in @cryptascreen/sdk)."""

    originator_name: str | None = Field(default=None, alias="originatorName")
    originator_account: str | None = Field(default=None, alias="originatorAccount")
    originator_vasp: str | None = Field(default=None, alias="originatorVasp")
    transfer_amount: float | None = Field(default=None, alias="transferAmount")
    currency: str | None = None
    tx_hash: str | None = Field(default=None, alias="txHash")
    chain: str | None = None
    timestamp: str | None = None
    ivms101: dict[str, Any] | None = None


class VaspIdentification(CsModel):
    """VaspIdentification (see types/compliance.ts in @cryptascreen/sdk)."""

    identified: bool | None = None
    vasp_name: str | None = None
    jurisdiction: str | None = None
    mica_registered: bool | None = None
    travel_rule_protocol: str | None = None


class Dac8OperatorInfo(CsModel):
    """Dac8OperatorInfo (see types/compliance.ts in @cryptascreen/sdk)."""

    name: str
    tin: str
    tin_issued_by: str | None = Field(default=None, alias="tinIssuedBy")
    registration_number: str | None = Field(default=None, alias="registrationNumber")
    address: str | None = None
    country: str


class Dac8TransactionData(CsModel):
    """Dac8TransactionData (see types/compliance.ts in @cryptascreen/sdk)."""

    tx_hash: str | None = Field(default=None, alias="txHash")
    chain: str | None = None
    transaction_date: str = Field(alias="transactionDate")
    transaction_type: str = Field(alias="transactionType")
    crypto_asset: str = Field(alias="cryptoAsset")
    units: float
    fmv_at_transaction: float | None = Field(default=None, alias="fmvAtTransaction")


class Dac8UserData(CsModel):
    """Dac8UserData (see types/compliance.ts in @cryptascreen/sdk)."""

    user_id: str = Field(alias="userId")
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    entity_name: str | None = Field(default=None, alias="entityName")
    tin: str | None = None
    residence_country: str = Field(alias="residenceCountry")
    transactions: list[Dac8TransactionData] | None = None


class Dac8ReportRequest(CsModel):
    """Dac8ReportRequest (see types/compliance.ts in @cryptascreen/sdk)."""

    tax_year: int = Field(alias="taxYear")
    jurisdiction: str
    operator: Dac8OperatorInfo
    users: list[Dac8UserData]


class Dac8ReportResult(CsModel):
    """Dac8ReportResult (see types/compliance.ts in @cryptascreen/sdk)."""

    report_id: str | None = Field(default=None, alias="reportId")
    transaction_count: int | None = Field(default=None, alias="transactionCount")
    generated_at: str | None = Field(default=None, alias="generatedAt")
    status: str | None = None
    xml_preview: str | None = Field(default=None, alias="xmlPreview")


class GraphRequest(CsModel):
    """GraphRequest (see types/graph.ts in @cryptascreen/sdk)."""

    seed_address: str = Field(alias="seedAddress")
    chain: str
    direction: str | None = None
    max_hops: int | None = Field(default=None, alias="maxHops")
    max_nodes: float | None = Field(default=None, alias="maxNodes")
    min_value_usd: float | None = Field(default=None, alias="minValueUsd")
    date_from: str | None = Field(default=None, alias="dateFrom")
    date_to: str | None = Field(default=None, alias="dateTo")
    aggregate_edges: bool | None = Field(default=None, alias="aggregateEdges")
    force_refresh: bool | None = Field(default=None, alias="forceRefresh")
    time_ordered: bool | None = Field(default=None, alias="timeOrdered")


class GraphNode(CsModel):
    """GraphNode (see types/graph.ts in @cryptascreen/sdk)."""

    id: str | None = None
    address: str | None = None
    chain: str | None = None
    label: str | None = None
    category: str | None = None
    risk_score: float | None = Field(default=None, alias="riskScore")
    risk_level: str | None = Field(default=None, alias="riskLevel")
    sanctions_match: bool | None = Field(default=None, alias="sanctionsMatch")
    flag_types: list[str] | None = Field(default=None, alias="flagTypes")
    is_seed: bool | None = Field(default=None, alias="isSeed")
    is_flagged: bool | None = Field(default=None, alias="isFlagged")
    total_inbound_usd: float | None = Field(default=None, alias="totalInboundUsd")
    total_outbound_usd: float | None = Field(default=None, alias="totalOutboundUsd")
    tx_count: int | None = Field(default=None, alias="txCount")
    first_seen: str | None = Field(default=None, alias="firstSeen")
    last_seen: str | None = Field(default=None, alias="lastSeen")
    hop: int | None = None
    scope_status: str | None = Field(default=None, alias="scopeStatus")


class GraphEdge(CsModel):
    """GraphEdge (see types/graph.ts in @cryptascreen/sdk)."""

    id: str | None = None
    source: str | None = None
    target: str | None = None
    tx_hash: str | None = Field(default=None, alias="txHash")
    chain: str | None = None
    value_usd: float | None = Field(default=None, alias="valueUsd")
    value_native: float | None = Field(default=None, alias="valueNative")
    asset_symbol: str | None = Field(default=None, alias="assetSymbol")
    timestamp: str | None = None
    tx_count: int | None = Field(default=None, alias="txCount")
    is_aggregated: bool | None = Field(default=None, alias="isAggregated")
    hop: int | None = None
    first_block: float | None = Field(default=None, alias="firstBlock")
    last_block: float | None = Field(default=None, alias="lastBlock")
    scope_status: str | None = Field(default=None, alias="scopeStatus")


class GraphStats(CsModel):
    """GraphStats (see types/graph.ts in @cryptascreen/sdk)."""

    total_nodes: float | None = Field(default=None, alias="totalNodes")
    total_edges: float | None = Field(default=None, alias="totalEdges")
    flagged_nodes: float | None = Field(default=None, alias="flaggedNodes")
    sanctioned_nodes: float | None = Field(default=None, alias="sanctionedNodes")
    total_value_traced_usd: float | None = Field(default=None, alias="totalValueTracedUsd")
    max_hops_reached: int | None = Field(default=None, alias="maxHopsReached")
    truncated: bool | None = None
    status: str | None = None
    status_reasons: list[str] | None = Field(default=None, alias="statusReasons")
    node_cap: float | None = Field(default=None, alias="nodeCap")


class GraphScope(CsModel):
    """GraphScope (see types/graph.ts in @cryptascreen/sdk)."""

    chain: str | None = None
    direction: str | None = None
    date_from: str | None = Field(default=None, alias="dateFrom")
    date_to: str | None = Field(default=None, alias="dateTo")
    max_hops: int | None = Field(default=None, alias="maxHops")
    time_ordered: bool | None = Field(default=None, alias="timeOrdered")
    finalized_block: float | None = Field(default=None, alias="finalizedBlock")
    provider: str | None = None


class GraphResponse(CsModel):
    """GraphResponse (see types/graph.ts in @cryptascreen/sdk)."""

    seed_address: str | None = Field(default=None, alias="seedAddress")
    chain: str | None = None
    nodes: list[GraphNode] | None = None
    edges: list[GraphEdge] | None = None
    flagged_node_ids: list[str] | None = Field(default=None, alias="flaggedNodeIds")
    sanctioned_node_ids: list[str] | None = Field(default=None, alias="sanctionedNodeIds")
    stats: GraphStats | None = None
    scope: GraphScope | None = None
    generated_at: str | None = Field(default=None, alias="generatedAt")


class EntityLabel(CsModel):
    """EntityLabel (see types/intelligence.ts in @cryptascreen/sdk)."""

    id: int | None = None
    address: str | None = None
    chain: str | None = None
    label: str | None = None
    category: str | None = None
    subcategory: str | None = None
    confidence: float | None = None
    source: str | None = None
    verified: bool | None = None
    first_seen: str | None = Field(default=None, alias="firstSeen")
    last_seen: str | None = Field(default=None, alias="lastSeen")
    metadata: str | None = None
    ingested_at: str | None = Field(default=None, alias="ingestedAt")
    valid_to: str | None = Field(default=None, alias="validTo")
    review_status: str | None = Field(default=None, alias="reviewStatus")


class VaspInfo(CsModel):
    """VaspInfo (see types/intelligence.ts in @cryptascreen/sdk)."""

    vasp_id: str | None = Field(default=None, alias="vaspId")
    name: str | None = None
    website: str | None = None
    jurisdiction: str | None = None
    regulatory_status: str | None = Field(default=None, alias="regulatoryStatus")
    supported_chains: list[str] | None = Field(default=None, alias="supportedChains")
    known_addresses: list[Any] | None = Field(default=None, alias="knownAddresses")
    risk_score: float | None = Field(default=None, alias="riskScore")
    updated_at: str | None = Field(default=None, alias="updatedAt")


class NameIdentifier(CsModel):
    """NameIdentifier (see types/names.ts in @cryptascreen/sdk)."""

    type: str
    value: str
    country: str | None = None


class NameScreenRequest(CsModel):
    """NameScreenRequest (see types/names.ts in @cryptascreen/sdk)."""

    name: str
    type: str | None = None
    aliases: list[str] | None = None
    date_of_birth: str | None = Field(default=None, alias="dateOfBirth")
    nationalities: list[str] | None = None
    country: str | None = None
    identifiers: list[NameIdentifier] | None = None
    monitor: bool | None = None


class NameListedEntity(CsModel):
    """NameListedEntity (see types/names.ts in @cryptascreen/sdk)."""

    source: str | None = None
    subject_id: str | None = Field(default=None, alias="subjectId")
    name: str | None = None
    type: str | None = None
    programs: list[str] | None = None
    listed_date: str | None = Field(default=None, alias="listedDate")


class NameMatchReason(CsModel):
    """NameMatchReason (see types/names.ts in @cryptascreen/sdk)."""

    field: str | None = None
    outcome: str | None = None
    points: int | None = None
    detail: str | None = None


class NameMatchDecision(CsModel):
    """NameMatchDecision (see types/names.ts in @cryptascreen/sdk)."""

    value: str | None = None
    reason: str | None = None
    decided_by: str | None = Field(default=None, alias="decidedBy")
    decided_at: str | None = Field(default=None, alias="decidedAt")
    auto_applied: bool | None = Field(default=None, alias="autoApplied")


class NameHit(CsModel):
    """NameHit (see types/names.ts in @cryptascreen/sdk)."""

    hit_id: str | None = Field(default=None, alias="hitId")
    listed_entity: NameListedEntity | None = Field(default=None, alias="listedEntity")
    score: float | None = None
    name_score: float | None = Field(default=None, alias="nameScore")
    matched_name: str | None = Field(default=None, alias="matchedName")
    matched_alias_quality: str | None = Field(default=None, alias="matchedAliasQuality")
    matched_fields: list[str] | None = Field(default=None, alias="matchedFields")
    conflict_fields: list[str] | None = Field(default=None, alias="conflictFields")
    reasons: list[NameMatchReason] | None = None
    explanation: str | None = None
    engine_decision: str | None = Field(default=None, alias="engineDecision")
    list_version: str | None = Field(default=None, alias="listVersion")
    decision: NameMatchDecision | None = None


class NameCoverage(CsModel):
    """NameCoverage (see types/names.ts in @cryptascreen/sdk)."""

    source: str | None = None
    state: str | None = None
    reason: str | None = None


class NameScreenResponse(CsModel):
    """NameScreenResponse (see types/names.ts in @cryptascreen/sdk)."""

    screening_id: str | None = Field(default=None, alias="screeningId")
    subject_ref: str | None = Field(default=None, alias="subjectRef")
    outcome: str | None = None
    list_match: str | None = Field(default=None, alias="listMatch")
    policy_version: str | None = Field(default=None, alias="policyVersion")
    strength: str | None = None
    threshold: float | None = None
    lists_version: dict[str, str] | None = Field(default=None, alias="listsVersion")
    coverage: list[NameCoverage] | None = None
    hits: list[NameHit] | None = None
    case_ref: str | None = Field(default=None, alias="caseRef")
    created_at: str | None = Field(default=None, alias="createdAt")
    replayed: bool | None = None


class NameDecisionRequest(CsModel):
    """NameDecisionRequest (see types/names.ts in @cryptascreen/sdk)."""

    hit_id: str = Field(alias="hitId")
    value: str
    reason: str


class NameScreenOptions(CsModel):
    """NameScreenOptions (see types/names.ts in @cryptascreen/sdk)."""

    idempotency_key: str | None = Field(default=None, alias="idempotencyKey")


class NameScreeningHistoryItem(CsModel):
    """NameScreeningHistoryItem (see types/names.ts in @cryptascreen/sdk)."""

    screening_id: str | None = Field(default=None, alias="screeningId")
    created_at: str | None = Field(default=None, alias="createdAt")
    origin: str | None = None
    actor: str | None = None
    name: str | None = None
    outcome: str | None = None
    top_score: float | None = Field(default=None, alias="topScore")
    hit_count: int | None = Field(default=None, alias="hitCount")
    case_ref: str | None = Field(default=None, alias="caseRef")


class SanctionsCheckResponse(CsModel):
    """SanctionsCheckResponse (see types/sanctions.ts in @cryptascreen/sdk)."""

    address: str | None = None
    chain: str | None = None
    match: bool | None = None
    list_name: str | None = Field(default=None, alias="listName")
    entity_name: str | None = Field(default=None, alias="entityName")
    program: str | None = None
    sanction_type: str | None = Field(default=None, alias="sanctionType")
    confidence: float | None = None
    canonical_chain: str | None = Field(default=None, alias="canonicalChain")
    blocking: bool | None = None
    candidate: bool | None = None
    match_state: str | None = Field(default=None, alias="matchState")
    disposition: str | None = None
    issuer: str | None = None
    restriction_type: str | None = Field(default=None, alias="restrictionType")
    programs: list[str] | None = None
    subject_id: str | None = Field(default=None, alias="subjectId")
    findings: list[ScreeningFlag] | None = None
    layer: ScreeningLayer | None = None
    review: ReviewStatus | None = None
    policy_version: str | None = Field(default=None, alias="policyVersion")


class SanctionsStatusResponse(CsModel):
    """SanctionsStatusResponse (see types/sanctions.ts in @cryptascreen/sdk)."""

    total_active: float | None = None
    by_source: dict[str, float] | None = None
    last_checked: str | None = None


class HeuristicDetectorStatus(CsModel):
    """HeuristicDetectorStatus (see types/screening.ts in @cryptascreen/sdk)."""

    detector: str | None = None
    outcome: str | None = None
    reason: str | None = None
    missing_capabilities: list[str] | None = Field(default=None, alias="missingCapabilities")
    flag_count: int | None = Field(default=None, alias="flagCount")


class SourceFreshness(CsModel):
    """SourceFreshness (see types/screening.ts in @cryptascreen/sdk)."""

    source_id: str | None = Field(default=None, alias="sourceId")
    issuer: str | None = None
    list_name: str | None = Field(default=None, alias="listName")
    required: bool | None = None
    fetch_enabled: bool | None = Field(default=None, alias="fetchEnabled")
    freshness_state: str | None = Field(default=None, alias="freshnessState")
    stale_reason: str | None = Field(default=None, alias="staleReason")
    snapshot_version: int | None = Field(default=None, alias="snapshotVersion")
    snapshot_hash: str | None = Field(default=None, alias="snapshotHash")
    published_at: str | None = Field(default=None, alias="publishedAt")
    last_success_at: str | None = Field(default=None, alias="lastSuccessAt")
    error_state: str | None = Field(default=None, alias="errorState")


class ScreeningLayer(CsModel):
    """ScreeningLayer (see types/screening.ts in @cryptascreen/sdk)."""

    state: str | None = None
    reason: str | None = None
    checked: bool | None = None
    findings: float | None = None
    sources: list[SourceFreshness] | None = None
    provider: str | None = None
    missing_capabilities: list[str] | None = Field(default=None, alias="missingCapabilities")
    truncated: bool | None = None
    truncation_reasons: list[str] | None = Field(default=None, alias="truncationReasons")


class ScreeningLayers(CsModel):
    """ScreeningLayers (see types/screening.ts in @cryptascreen/sdk)."""

    sanctions: ScreeningLayer | None = None
    threat_intel: ScreeningLayer | None = Field(default=None, alias="threatIntel")
    entity: ScreeningLayer | None = None
    on_chain: ScreeningLayer | None = Field(default=None, alias="onChain")


class ReviewStatus(CsModel):
    """ReviewStatus (see types/screening.ts in @cryptascreen/sdk)."""

    status: str | None = None
    decision_id: int | None = Field(default=None, alias="decisionId")
    decision_type: str | None = Field(default=None, alias="decisionType")
    effect: str | None = None
    reason: str | None = None
    actor: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    expires_at: str | None = Field(default=None, alias="expiresAt")
    revoked_at: str | None = Field(default=None, alias="revokedAt")
    alert_routing_suppressed: bool | None = Field(default=None, alias="alertRoutingSuppressed")
    blocking_finding_preserved: bool | None = Field(default=None, alias="blockingFindingPreserved")


class ScreeningFlag(CsModel):
    """ScreeningFlag (see types/screening.ts in @cryptascreen/sdk)."""

    flag_type: str | None = Field(default=None, alias="flagType")
    description: str | None = None
    hop_distance: int | None = Field(default=None, alias="hopDistance")
    confidence: float | None = None
    source: str | None = None
    source_address: str | None = Field(default=None, alias="sourceAddress")
    source_sanction_type: str | None = Field(default=None, alias="sourceSanctionType")
    source_entity: str | None = Field(default=None, alias="sourceEntity")
    category: str | None = None
    match_state: str | None = Field(default=None, alias="matchState")
    blocking: bool | None = None
    context_only: bool | None = Field(default=None, alias="contextOnly")
    score_contribution: float | None = Field(default=None, alias="scoreContribution")
    dedup_key: str | None = Field(default=None, alias="dedupKey")
    counted: bool | None = None
    policy_reason: str | None = Field(default=None, alias="policyReason")
    policy_version: str | None = Field(default=None, alias="policyVersion")
    source_id: str | None = Field(default=None, alias="sourceId")
    issuer: str | None = None
    list_name: str | None = Field(default=None, alias="listName")
    programs: list[str] | None = None
    restriction_type: str | None = Field(default=None, alias="restrictionType")
    subject_id: str | None = Field(default=None, alias="subjectId")
    alias_ids: str | None = Field(default=None, alias="aliasIds")
    currency_tag: str | None = Field(default=None, alias="currencyTag")
    chain_basis: str | None = Field(default=None, alias="chainBasis")
    match_quality: str | None = Field(default=None, alias="matchQuality")
    valid_from: str | None = Field(default=None, alias="validFrom")
    valid_to: str | None = Field(default=None, alias="validTo")
    snapshot_id: int | None = Field(default=None, alias="snapshotId")
    snapshot_version: int | None = Field(default=None, alias="snapshotVersion")


class ScreeningResponse(CsModel):
    """ScreeningResponse (see types/screening.ts in @cryptascreen/sdk)."""

    address: str | None = None
    chain: str | None = None
    coverage: str | None = None
    risk_score: float | None = Field(default=None, alias="riskScore")
    risk_level: str | None = Field(default=None, alias="riskLevel")
    sanctions_match: bool | None = Field(default=None, alias="sanctionsMatch")
    entity_label: str | None = Field(default=None, alias="entityLabel")
    entity_category: str | None = Field(default=None, alias="entityCategory")
    confidence: float | None = None
    flags: list[ScreeningFlag] | None = None
    screening_providers_used: list[str] | None = Field(default=None, alias="screeningProvidersUsed")
    screened_at: str | None = Field(default=None, alias="screenedAt")
    cache_hit: bool | None = Field(default=None, alias="cacheHit")
    heuristics_status: str | None = Field(default=None, alias="heuristicsStatus")
    heuristics_job_id: str | None = Field(default=None, alias="heuristicsJobId")
    heuristics_detectors: list[HeuristicDetectorStatus] | None = Field(
        default=None, alias="heuristicsDetectors"
    )
    policy_version: str | None = Field(default=None, alias="policyVersion")
    score_version: str | None = Field(default=None, alias="scoreVersion")
    blocking_match: bool | None = Field(default=None, alias="blockingMatch")
    disposition: str | None = None
    assessment_status: str | None = Field(default=None, alias="assessmentStatus")
    checked_layers: list[str] | None = Field(default=None, alias="checkedLayers")
    layers: ScreeningLayers | None = None
    review: ReviewStatus | None = None
    evidence_version: str | None = Field(default=None, alias="evidenceVersion")
    validity: ResultValidity | None = None
    evaluation_id: str | None = Field(default=None, alias="evaluationId")
    vendor_layers: list[VendorLayer] | None = Field(default=None, alias="vendorLayers")


class VendorLayer(CsModel):
    """VendorLayer (see types/screening.ts in @cryptascreen/sdk)."""

    vendor: str | None = None
    status: str | None = None
    fetched_at: str | None = Field(default=None, alias="fetchedAt")
    cached: bool | None = None
    rating: str | None = None
    rating_scale: str | None = Field(default=None, alias="ratingScale")
    categories: list[str] | None = None
    reasons: list[str] | None = None
    attribution: str | None = None


class ResultValidity(CsModel):
    """ResultValidity (see types/screening.ts in @cryptascreen/sdk)."""

    evidence_version: str | None = Field(default=None, alias="evidenceVersion")
    cache_decision: str | None = Field(default=None, alias="cacheDecision")
    mode: str | None = None
    include_heuristics: bool | None = Field(default=None, alias="includeHeuristics")
    address_evidence_version: int | None = Field(default=None, alias="addressEvidenceVersion")
    entity_label_version: int | None = Field(default=None, alias="entityLabelVersion")
    source_snapshot_versions: dict[str, float | None] | None = Field(
        default=None, alias="sourceSnapshotVersions"
    )
    tenant_policy_version: int | None = Field(default=None, alias="tenantPolicyVersion")
    policy_version: str | None = Field(default=None, alias="policyVersion")
    score_version: str | None = Field(default=None, alias="scoreVersion")
    chain_provider: str | None = Field(default=None, alias="chainProvider")
    entitlements: str | None = None
    computed_at: str | None = Field(default=None, alias="computedAt")
    result_age_seconds: float | None = Field(default=None, alias="resultAgeSeconds")
    source_age_seconds: dict[str, float | None] | None = Field(
        default=None, alias="sourceAgeSeconds"
    )
    oldest_required_source_age_seconds: float | None = Field(
        default=None, alias="oldestRequiredSourceAgeSeconds"
    )
    tier0_lookup: str | None = Field(default=None, alias="tier0Lookup")


class ScreeningEvaluation(CsModel):
    """ScreeningEvaluation (see types/screening.ts in @cryptascreen/sdk)."""

    evaluation_id: str | None = Field(default=None, alias="evaluationId")
    job_id: str | None = Field(default=None, alias="jobId")
    origin: str | None = None
    actor: Any = None
    input: Any = None
    evaluated_at: str | None = Field(default=None, alias="evaluatedAt")
    risk_score: float | None = Field(default=None, alias="riskScore")
    risk_level: str | None = Field(default=None, alias="riskLevel")
    assessment_status: str | None = Field(default=None, alias="assessmentStatus")
    disposition: str | None = None
    coverage: str | None = None
    sanctions_match: bool | None = Field(default=None, alias="sanctionsMatch")
    blocking_match: bool | None = Field(default=None, alias="blockingMatch")
    cache_hit: bool | None = Field(default=None, alias="cacheHit")
    policy_version: str | None = Field(default=None, alias="policyVersion")
    score_version: str | None = Field(default=None, alias="scoreVersion")
    scope: Any = None
    evidence: Any = None
    result: ScreeningResponse | None = None
    supersession: Any = None
    latest: bool | None = None
    integrity: Any = None
    retention: Any = None


class ScreeningEvaluationPage(CsModel):
    """ScreeningEvaluationPage (see types/screening.ts in @cryptascreen/sdk)."""

    items: list[ScreeningEvaluation] | None = None
    page: int | None = None
    size: int | None = None
    total_elements: int | None = Field(default=None, alias="totalElements")
    total_pages: int | None = Field(default=None, alias="totalPages")
    latest_evaluation_id: str | None = Field(default=None, alias="latestEvaluationId")


class ScreenAddressRequest(CsModel):
    """ScreenAddressRequest (see types/screening.ts in @cryptascreen/sdk)."""

    address: str
    chain: str
    include_heuristics: bool | None = Field(default=None, alias="includeHeuristics")
    force_refresh: bool | None = Field(default=None, alias="forceRefresh")
    mode: str | None = None


class BulkScreeningRequest(CsModel):
    """BulkScreeningRequest (see types/screening.ts in @cryptascreen/sdk)."""

    addresses: list[str]
    chains: list[str]
    async_: bool | None = Field(default=None, alias="async")
    names: list[Any] | None = None


class ScreeningJobSummary(CsModel):
    """ScreeningJobSummary (see types/screening.ts in @cryptascreen/sdk)."""

    high_risk_addresses: list[str] | None = Field(default=None, alias="highRiskAddresses")
    critical_addresses: list[str] | None = Field(default=None, alias="criticalAddresses")
    sanctioned_addresses: list[str] | None = Field(default=None, alias="sanctionedAddresses")


class ScreeningJob(CsModel):
    """ScreeningJob (see types/screening.ts in @cryptascreen/sdk)."""

    job_id: str | None = Field(default=None, alias="jobId")
    status: str | None = None
    total: int | None = None
    processed: float | None = None
    succeeded: float | None = None
    failed: float | None = None
    results: list[ScreeningResponse] | None = None
    summary: ScreeningJobSummary | None = None
    error: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    started_at: str | None = Field(default=None, alias="startedAt")
    completed_at: str | None = Field(default=None, alias="completedAt")
    error_code: str | None = Field(default=None, alias="errorCode")
    cancel_requested: bool | None = Field(default=None, alias="cancelRequested")
    results_url: str | None = Field(default=None, alias="resultsUrl")
    policy_version: str | None = Field(default=None, alias="policyVersion")
    score_version: str | None = Field(default=None, alias="scoreVersion")


class ScreeningJobItem(CsModel):
    """ScreeningJobItem (see types/screening.ts in @cryptascreen/sdk)."""

    index: int | None = None
    address: str | None = None
    chain: str | None = None
    status: str | None = None
    evaluation_id: str | None = Field(default=None, alias="evaluationId")
    risk_level: str | None = Field(default=None, alias="riskLevel")
    risk_score: float | None = Field(default=None, alias="riskScore")
    sanctions_match: bool | None = Field(default=None, alias="sanctionsMatch")
    result: ScreeningResponse | None = None
    error_code: str | None = Field(default=None, alias="errorCode")
    created_at: str | None = Field(default=None, alias="createdAt")


class AsyncSubmitOptions(CsModel):
    """AsyncSubmitOptions (see types/screening.ts in @cryptascreen/sdk)."""

    idempotency_key: str | None = Field(default=None, alias="idempotencyKey")


class ScreeningJobResultsPage(CsModel):
    """ScreeningJobResultsPage (see types/screening.ts in @cryptascreen/sdk)."""

    job_id: str | None = Field(default=None, alias="jobId")
    status: str | None = None
    items: list[ScreeningJobItem] | None = None
    page: int | None = None
    size: int | None = None
    total_items: int | None = Field(default=None, alias="totalItems")
    total_pages: int | None = Field(default=None, alias="totalPages")


class PageOptions(CsModel):
    """PageOptions (see types/screening.ts in @cryptascreen/sdk)."""

    page: int | None = None
    size: int | None = None


class WalletTransferCount(CsModel):
    """WalletTransferCount (see types/wallet.ts in @cryptascreen/sdk)."""

    value: float | None = None
    basis: str | None = None


class WalletSectionStatus(CsModel):
    """WalletSectionStatus (see types/wallet.ts in @cryptascreen/sdk)."""

    state: str | None = None
    reason_code: str | None = Field(default=None, alias="reasonCode")
    detail: str | None = None
    provider: str | None = None
    window_from: str | None = Field(default=None, alias="windowFrom")
    window_to: str | None = Field(default=None, alias="windowTo")
    events_read: float | None = Field(default=None, alias="eventsRead")
    pages_used: float | None = Field(default=None, alias="pagesUsed")
    transfer_count: WalletTransferCount | None = Field(default=None, alias="transferCount")


class WalletListing(CsModel):
    """WalletListing (see types/wallet.ts in @cryptascreen/sdk)."""

    category: str | None = None
    source_id: str | None = Field(default=None, alias="sourceId")
    list_type: str | None = Field(default=None, alias="listType")
    entity_name: str | None = Field(default=None, alias="entityName")
    program: str | None = None


class WalletAssetTotal(CsModel):
    """WalletAssetTotal (see types/wallet.ts in @cryptascreen/sdk)."""

    asset: str | None = None
    symbol: str | None = None
    received: Any = None
    sent: Any = None
    tx_count: int | None = Field(default=None, alias="txCount")


class WalletFiat(CsModel):
    """WalletFiat (see types/wallet.ts in @cryptascreen/sdk)."""

    currency: str | None = None
    state: str | None = None
    received: Any = None
    sent: Any = None
    total: Any = None
    priced_tx_count: int | None = Field(default=None, alias="pricedTxCount")
    unpriced_tx_count: int | None = Field(default=None, alias="unpricedTxCount")


class WalletCounterparty(CsModel):
    """WalletCounterparty (see types/wallet.ts in @cryptascreen/sdk)."""

    address: str | None = None
    direction: str | None = None
    tx_count: int | None = Field(default=None, alias="txCount")
    in_count: int | None = Field(default=None, alias="inCount")
    out_count: int | None = Field(default=None, alias="outCount")
    assets: list[WalletAssetTotal] | None = None
    fiat: WalletFiat | None = None
    first_seen: str | None = Field(default=None, alias="firstSeen")
    last_seen: str | None = Field(default=None, alias="lastSeen")
    listed: bool | None = None
    listings: list[WalletListing] | None = None


class WalletCounterpartyPage(CsModel):
    """WalletCounterpartyPage (see types/wallet.ts in @cryptascreen/sdk)."""

    unpriced_assets: list[str] | None = Field(default=None, alias="unpricedAssets")
    items: list[WalletCounterparty] | None = None


class WalletTransaction(CsModel):
    """WalletTransaction (see types/wallet.ts in @cryptascreen/sdk)."""

    tx_hash: str | None = Field(default=None, alias="txHash")
    time: str | None = None
    direction: str | None = None
    counterparty: str | None = None
    asset: str | None = None
    symbol: str | None = None
    amount: Any = None
    fiat_usd: Any = Field(default=None, alias="fiatUsd")
    priced: bool | None = None
    category: str | None = None
    internal: bool | None = None
    log_index: int | None = Field(default=None, alias="logIndex")
    block_number: float | None = Field(default=None, alias="blockNumber")
    explorer_url: str | None = Field(default=None, alias="explorerUrl")
    counterparty_listed: bool | None = Field(default=None, alias="counterpartyListed")
    kind: str | None = None
    token_id: str | None = Field(default=None, alias="tokenId")
    protocol_income: bool | None = Field(default=None, alias="protocolIncome")


class WalletTransactionPage(CsModel):
    """WalletTransactionPage (see types/wallet.ts in @cryptascreen/sdk)."""

    items: list[WalletTransaction] | None = None


class WalletPathStep(CsModel):
    """WalletPathStep (see types/wallet.ts in @cryptascreen/sdk)."""

    index: int | None = None
    from_: str | None = Field(default=None, alias="from")
    to: str | None = None
    tx_hash: str | None = Field(default=None, alias="txHash")
    time: str | None = None
    asset: str | None = None
    symbol: str | None = None
    amount: Any = None
    fiat_usd: Any = Field(default=None, alias="fiatUsd")
    edge_tx_count: int | None = Field(default=None, alias="edgeTxCount")
    explorer_url: str | None = Field(default=None, alias="explorerUrl")


class WalletExposureHit(CsModel):
    """WalletExposureHit (see types/wallet.ts in @cryptascreen/sdk)."""

    hop: int | None = None
    counterparty: str | None = None
    category: str | None = None
    direction: str | None = None
    listings: list[WalletListing] | None = None
    steps: list[WalletPathStep] | None = None


class WalletUsdShare(CsModel):
    """WalletUsdShare (see types/wallet.ts in @cryptascreen/sdk)."""

    total: Any = None
    direct: Any = None
    within_hops: Any = Field(default=None, alias="withinHops")
    direct_share: Any = Field(default=None, alias="directShare")
    within_hops_share: Any = Field(default=None, alias="withinHopsShare")
    priced_tx_count: int | None = Field(default=None, alias="pricedTxCount")
    unpriced_tx_count: int | None = Field(default=None, alias="unpricedTxCount")


class WalletAssetShare(CsModel):
    """WalletAssetShare (see types/wallet.ts in @cryptascreen/sdk)."""

    asset: str | None = None
    symbol: str | None = None
    total: Any = None
    direct: Any = None
    within_hops: Any = Field(default=None, alias="withinHops")
    direct_share: Any = Field(default=None, alias="directShare")
    within_hops_share: Any = Field(default=None, alias="withinHopsShare")
    tx_count: int | None = Field(default=None, alias="txCount")


class WalletDirectionShare(CsModel):
    """WalletDirectionShare (see types/wallet.ts in @cryptascreen/sdk)."""

    flow: str | None = None
    usd: WalletUsdShare | None = None
    by_asset: list[WalletAssetShare] | None = Field(default=None, alias="byAsset")


class WalletShareOfValue(CsModel):
    """WalletShareOfValue (see types/wallet.ts in @cryptascreen/sdk)."""

    method: str | None = None
    max_hops: int | None = Field(default=None, alias="maxHops")
    window_from: str | None = Field(default=None, alias="windowFrom")
    window_to: str | None = Field(default=None, alias="windowTo")
    received: WalletDirectionShare | None = None
    sent: WalletDirectionShare | None = None


class WalletCategoryAssetShare(CsModel):
    """WalletCategoryAssetShare (see types/wallet.ts in @cryptascreen/sdk)."""

    asset: str | None = None
    symbol: str | None = None
    units: Any = None
    asset_total: Any = Field(default=None, alias="assetTotal")
    share: Any = None


class WalletCategoryPart(CsModel):
    """WalletCategoryPart (see types/wallet.ts in @cryptascreen/sdk)."""

    state: str | None = None
    reason_code: str | None = Field(default=None, alias="reasonCode")
    usd: Any = None
    usd_share: Any = Field(default=None, alias="usdShare")
    tx_count: int | None = Field(default=None, alias="txCount")
    by_asset: list[WalletCategoryAssetShare] | None = Field(default=None, alias="byAsset")


class WalletCategoryShare(CsModel):
    """WalletCategoryShare (see types/wallet.ts in @cryptascreen/sdk)."""

    category: str | None = None
    direct: WalletCategoryPart | None = None
    indirect: WalletCategoryPart | None = None


class WalletCategoryAssetTotal(CsModel):
    """WalletCategoryAssetTotal (see types/wallet.ts in @cryptascreen/sdk)."""

    asset: str | None = None
    symbol: str | None = None
    total: Any = None
    tx_count: int | None = Field(default=None, alias="txCount")


class WalletCategoryFlow(CsModel):
    """WalletCategoryFlow (see types/wallet.ts in @cryptascreen/sdk)."""

    flow: str | None = None
    usd_total: Any = Field(default=None, alias="usdTotal")
    priced_tx_count: int | None = Field(default=None, alias="pricedTxCount")
    unpriced_tx_count: int | None = Field(default=None, alias="unpricedTxCount")
    asset_totals: list[WalletCategoryAssetTotal] | None = Field(default=None, alias="assetTotals")
    categories: list[WalletCategoryShare] | None = None
    any_direct: WalletCategoryPart | None = Field(default=None, alias="anyDirect")
    any_indirect: WalletCategoryPart | None = Field(default=None, alias="anyIndirect")
    protocol_income: WalletCategoryPart | None = Field(default=None, alias="protocolIncome")


class WalletCategoryDerivedSource(CsModel):
    """WalletCategoryDerivedSource (see types/wallet.ts in @cryptascreen/sdk)."""

    id: str | None = None
    state: str | None = None
    reason_code: str | None = Field(default=None, alias="reasonCode")
    entries: float | None = None


class WalletCategoryExposure(CsModel):
    """WalletCategoryExposure (see types/wallet.ts in @cryptascreen/sdk)."""

    method: str | None = None
    max_hops: int | None = Field(default=None, alias="maxHops")
    window_from: str | None = Field(default=None, alias="windowFrom")
    window_to: str | None = Field(default=None, alias="windowTo")
    section: WalletSectionStatus | None = None
    path_search: WalletSectionStatus | None = Field(default=None, alias="pathSearch")
    derived_sources: list[WalletCategoryDerivedSource] | None = Field(
        default=None, alias="derivedSources"
    )
    received: WalletCategoryFlow | None = None
    sent: WalletCategoryFlow | None = None


class WalletStolenAssetShare(CsModel):
    """WalletStolenAssetShare (see types/wallet.ts in @cryptascreen/sdk)."""

    symbol: str | None = None
    decimals: int | None = None
    stolen_raw: str | None = Field(default=None, alias="stolenRaw")
    received_raw: str | None = Field(default=None, alias="receivedRaw")
    share_pct: float | None = Field(default=None, alias="sharePct")
    priced: bool | None = None


class WalletDerivedStep(CsModel):
    """WalletDerivedStep (see types/wallet.ts in @cryptascreen/sdk)."""

    index: int | None = None
    from_: str | None = Field(default=None, alias="from")
    to: str | None = None
    tx_hash: str | None = Field(default=None, alias="txHash")
    block: float | None = None
    time: str | None = None
    asset: str | None = None
    symbol: str | None = None
    decimals: int | None = None
    amount_raw: str | None = Field(default=None, alias="amountRaw")
    stolen_raw: str | None = Field(default=None, alias="stolenRaw")
    share_at_receiver: float | None = Field(default=None, alias="shareAtReceiver")
    explorer_url: str | None = Field(default=None, alias="explorerUrl")


class WalletDerivedExposure(CsModel):
    """WalletDerivedExposure (see types/wallet.ts in @cryptascreen/sdk)."""

    hops: int | None = None
    share_pct: float | None = Field(default=None, alias="sharePct")
    category: str | None = None
    seed_source_id: str | None = Field(default=None, alias="seedSourceId")
    incident_id: str | None = Field(default=None, alias="incidentId")
    incident_date: str | None = Field(default=None, alias="incidentDate")
    incident_date_basis: str | None = Field(default=None, alias="incidentDateBasis")
    source_url: str | None = Field(default=None, alias="sourceUrl")
    source_published: str | None = Field(default=None, alias="sourcePublished")
    seed_address: str | None = Field(default=None, alias="seedAddress")
    completeness: str | None = None
    completeness_reason: str | None = Field(default=None, alias="completenessReason")
    partial_evidence: bool | None = Field(default=None, alias="partialEvidence")
    chain_confidence: float | None = Field(default=None, alias="chainConfidence")
    chain_note: str | None = Field(default=None, alias="chainNote")
    value_by_asset: dict[str, WalletStolenAssetShare] | None = Field(
        default=None, alias="valueByAsset"
    )
    value_usd: Any = Field(default=None, alias="valueUsd")
    first_received_at: str | None = Field(default=None, alias="firstReceivedAt")
    steps: list[WalletDerivedStep] | None = None
    points: int | None = None
    why: str | None = None
    trace_version: str | None = Field(default=None, alias="traceVersion")
    computed_at: str | None = Field(default=None, alias="computedAt")


class WalletStolenFundsTrace(CsModel):
    """WalletStolenFundsTrace (see types/wallet.ts in @cryptascreen/sdk)."""

    derived_from: str | None = Field(default=None, alias="derivedFrom")
    policy_version: str | None = Field(default=None, alias="policyVersion")
    points: int | None = None
    blocks: Any = None
    entries: list[WalletDerivedExposure] | None = None


class WalletExposurePaths(CsModel):
    """WalletExposurePaths (see types/wallet.ts in @cryptascreen/sdk)."""

    chain: str | None = None
    address: str | None = None
    evaluation_id: str | None = Field(default=None, alias="evaluationId")
    section: WalletSectionStatus | None = None
    path_search: WalletSectionStatus | None = Field(default=None, alias="pathSearch")
    max_hops: int | None = Field(default=None, alias="maxHops")
    share_of_value: WalletShareOfValue | None = Field(default=None, alias="shareOfValue")
    hit_count: int | None = Field(default=None, alias="hitCount")
    hits: list[WalletExposureHit] | None = None
    category_exposure: WalletCategoryExposure | None = Field(default=None, alias="categoryExposure")
    stolen_funds_trace: WalletStolenFundsTrace | None = Field(
        default=None, alias="stolenFundsTrace"
    )


class WalletSectionOptions(CsModel):
    """WalletSectionOptions (see types/wallet.ts in @cryptascreen/sdk)."""

    page: int | None = None
    size: int | None = None
    sort: str | None = None
    order: str | None = None
    days: int | None = None


class WalletCounterpartyOptions(WalletSectionOptions):
    """WalletCounterpartyOptions (see types/wallet.ts in @cryptascreen/sdk)."""

    direction: str | None = None
    listed_only: bool | None = Field(default=None, alias="listedOnly")


class WalletTransactionOptions(WalletSectionOptions):
    """WalletTransactionOptions (see types/wallet.ts in @cryptascreen/sdk)."""

    direction: str | None = None
    counterparty: str | None = None


class AlertReason(CsModel):
    """AlertReason (see types/wallet.ts in @cryptascreen/sdk)."""

    code: str | None = None
    params: dict[str, Any] | None = None


class AlertAcknowledgement(CsModel):
    """AlertAcknowledgement (see types/wallet.ts in @cryptascreen/sdk)."""

    at: str | None = None
    by: str | None = None
    user_id: int | None = Field(default=None, alias="userId")
    note: str | None = None


class AlertAuditEntry(CsModel):
    """AlertAuditEntry (see types/wallet.ts in @cryptascreen/sdk)."""

    event: str | None = None
    actor: str | None = None
    at: str | None = None
    note: str | None = None


class AlertDetail(CsModel):
    """AlertDetail (see types/wallet.ts in @cryptascreen/sdk)."""

    id: int | None = None
    address: str | None = None
    chain: str | None = None
    risk_level: str | None = Field(default=None, alias="riskLevel")
    alert_type: str | None = Field(default=None, alias="alertType")
    created_at: str | None = Field(default=None, alias="createdAt")
    reason_state: str | None = Field(default=None, alias="reasonState")
    reasons: list[AlertReason] | None = None
    evaluation_id: str | None = Field(default=None, alias="evaluationId")
    case_refs: list[str] | None = Field(default=None, alias="caseRefs")
    acknowledged: bool | None = None
    acknowledgement: AlertAcknowledgement | None = None
    audit_trail: list[AlertAuditEntry] | None = Field(default=None, alias="auditTrail")
    already_acknowledged: bool | None = Field(default=None, alias="alreadyAcknowledged")


class CaseAssignee(CsModel):
    """CaseAssignee (see types/wallet.ts in @cryptascreen/sdk)."""

    user_id: int | None = Field(default=None, alias="userId")
    name: str | None = None
    email: str | None = None
    assigned_at: str | None = Field(default=None, alias="assignedAt")
    assigned_by: str | None = Field(default=None, alias="assignedBy")


class CaseAssignment(CsModel):
    """CaseAssignment (see types/wallet.ts in @cryptascreen/sdk)."""

    case_ref: str | None = Field(default=None, alias="caseRef")
    assignee: CaseAssignee | None = None
    evaluation_ids: list[str] | None = Field(default=None, alias="evaluationIds")
    changed: bool | None = None


class WebhookConfig(CsModel):
    """A registered webhook endpoint as ``webhooks.list()`` returns it (the secret is only a hint)."""

    id: int | None = None
    url: str | None = None
    secret: str | None = None
    events: list[str] | None = None
    is_active: bool | None = Field(default=None, alias="isActive")
    description: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")


class WebhookDelivery(CsModel):
    """One delivery record of an endpoint (status PENDING | DELIVERED | FAILED | EXHAUSTED)."""

    id: str | None = None
    webhook_config_id: int | None = Field(default=None, alias="webhookConfigId")
    event_type: str | None = Field(default=None, alias="eventType")
    payload: dict[str, Any] | None = None
    status: str | None = None
    attempt_count: int | None = Field(default=None, alias="attemptCount")
    last_attempt_at: str | None = Field(default=None, alias="lastAttemptAt")
    next_retry_at: str | None = Field(default=None, alias="nextRetryAt")
    response_code: int | None = Field(default=None, alias="responseCode")
    response_body: str | None = Field(default=None, alias="responseBody")
    created_at: str | None = Field(default=None, alias="createdAt")
    delivered_at: str | None = Field(default=None, alias="deliveredAt")
    event_id: str | None = Field(default=None, alias="eventId")
    source_type: str | None = Field(default=None, alias="sourceType")
    source_id: str | None = Field(default=None, alias="sourceId")
    last_error: str | None = Field(default=None, alias="lastError")


# aliases kept from the TypeScript SDK
SanctionsCheckResult = SanctionsCheckResponse
PolicyVersion = str
ScreeningResult = ScreeningResponse

for _m in list(globals().values()):
    if isinstance(_m, type) and issubclass(_m, BaseModel) and _m is not BaseModel:
        _m.model_rebuild()
