from pydantic import BaseModel, Field, model_validator
from enum import Enum
from typing import Optional

class SubstructureType(str, Enum):
    cdm = "cdm"
    axion = "axion"
    no_sub = "no_sub"

class ModelType(str, Enum):
    Model_I = "Model_I"
    Model_II = "Model_II"
    Model_III = "Model_III"
    Model_IV = "Model_IV"

class SimulationConfig(BaseModel):
    model_type: ModelType = Field(
        description="MANDATORY: The user MUST explicitly state Model_I, Model_II, Model_III, or Model_IV. If missing, DO NOT CALL THIS TOOL."
    )
    substructure: SubstructureType = Field(
        description="MANDATORY: The user MUST specify cdm, axion, or no_sub. If missing, DO NOT CALL THIS TOOL."
    )
    main_halo_mass: float = Field(
        description="MANDATORY: The main halo mass (e.g., 1e12). If missing, DO NOT CALL THIS TOOL.",
        gt=0
    )
    axion_mass: Optional[float] = Field(
        default=1e-24,
        description="Optional: The mass of the axion. Only if substructure='axion'. Default 1e-24."
    )
    vortex_mass: Optional[float] = Field(
        default=1e10,
        description="Optional: The mass of the vortex. Only if substructure='axion'. Default 1e10."
    )
    z_halo: float = Field(
        description="MANDATORY: Lens redshift (e.g., 0.5). If missing, DO NOT CALL THIS TOOL."
    )
    z_gal: float = Field(
        description="MANDATORY: Source redshift (e.g., 1.0). If missing, DO NOT CALL THIS TOOL. Must be > z_halo and <= 1.0.",
        le=1.0
    )

    sigma_v: Optional[float] = Field(
        default=260.0,
        description="Velocity dispersion for Model_IV. Default 260."
    )
    source_pos_x: Optional[float] = Field(
        default=0.0,
        description="Source X position offset (arcsec). Default 0.0."
    )
    source_pos_y: Optional[float] = Field(
        default=0.0,
        description="Source Y position offset (arcsec). Default 0.0."
    )
    source_angle: Optional[float] = Field(
        default=0.0,
        description="Source rotation angle in radians. Default 0.0."
    )
    num_simulations: int = Field(
        default=1,
        description="Number of simulations to run. Default is 1.",
        ge=1,
        le=100
    )

    @model_validator(mode='after')
    def validate_redshifts(self) -> 'SimulationConfig':
        if self.z_gal <= self.z_halo:
            raise ValueError(f"Source redshift (z_gal={self.z_gal}) must be strictly greater than lens redshift (z_halo={self.z_halo})")
        return self

