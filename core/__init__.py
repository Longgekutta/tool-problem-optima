# -*- coding: utf-8 -*-
from .problemology import (
    FundamentalSpace,
    DivergenceType,
    SpaceCoordinates,
    ProblemDivergenceTensor,
    compute_tensor_divergence
)
from .tensor_model import (
    OntologicalAxis,
    AgencyAxis,
    AbstractionLayerAxis,
    ObservabilityAxis,
    RemediationAxis,
    ProblemTensor
)
from .pathology_catalog import (
    PathologyEntry,
    CATALOG,
    get_catalog_entry,
    list_all_entries
)

__all__ = [
    "FundamentalSpace",
    "DivergenceType",
    "SpaceCoordinates",
    "ProblemDivergenceTensor",
    "compute_tensor_divergence",
    "OntologicalAxis",
    "AgencyAxis",
    "AbstractionLayerAxis",
    "ObservabilityAxis",
    "RemediationAxis",
    "ProblemTensor",
    "PathologyEntry",
    "CATALOG",
    "get_catalog_entry",
    "list_all_entries"
]
