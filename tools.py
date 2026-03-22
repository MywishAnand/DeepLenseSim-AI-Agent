import os
import sys
import uuid
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from colossus.cosmology import cosmology
try:
    cosmology.setCosmology('planck15')
except Exception:
    pass

# Add DeepLenseSim to path so we can import it
sys.path.append(os.path.join(os.path.dirname(__file__), 'DeepLenseSim'))

try:
    from deeplense.lens import DeepLens
except ImportError as e:
    print(f"Failed to import DeepLens: {e}. Make sure lenstronomy and colossus are installed.")
    DeepLens = None

from schemas import SimulationConfig

def run_deeplensesim(config: SimulationConfig) -> dict:
    """
    Executes the DeepLenseSim pipeline using the given configuration.
    Generates images and returns their paths.
    """
    if DeepLens is None:
        return {"error": "DeepLenseSim or its dependencies are not properly installed."}

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    
    try:
        for i in range(config.num_simulations):
            # Initialize lens instance
            lens = DeepLens(
                axion_mass=config.axion_mass,
                z_halo=config.z_halo,
                z_gal=config.z_gal
            )
            
            # 1. Provide main halo mass
            lens.make_single_halo(config.main_halo_mass)
            
            # 2. Add substructure
            if config.substructure == "cdm":
                lens.make_old_cdm()
            elif config.substructure == "axion":
                lens.make_vortex(config.vortex_mass)
            elif config.substructure == "no_sub":
                lens.make_no_sub()
                
            # 3. Choose lighting model and instrument based on Model Type
            if config.model_type == "Model_I":
                lens.make_source_light()
                lens.simple_sim()
                image_data = lens.image_real
            elif config.model_type == "Model_II":
                lens.set_instrument('Euclid')
                lens.make_source_light_mag()
                lens.simple_sim_2()
                image_data = lens.image_real
            elif config.model_type == "Model_III":
                lens.set_instrument('hst')
                lens.make_source_light_mag()
                lens.simple_sim_2()
                image_data = lens.image_real
            elif config.model_type == "Model_IV":
                # Model IV logic ...
                from lenstronomy.SimulationAPI.ObservationConfig.Euclid import Euclid
                from lenstronomy.SimulationAPI.sim_api import SimAPI
                
                sim_g = SimAPI(numpix=64, kwargs_single_band=Euclid(band='VIS', coadd_years=6).kwargs_single_band(), kwargs_model={'lens_model_list': lens.lens_model_list, 'lens_redshift_list': lens.lens_redshift_list, 'source_light_model_list': ['SERSIC_ELLIPSE'], 'source_redshift_list': [config.z_gal], 'cosmo': lens.astropy_instance, 'z_source_convention': 2.5, 'z_source': 1.0})
                sim_r = SimAPI(numpix=64, kwargs_single_band=Euclid(band='VIS', coadd_years=6).kwargs_single_band(), kwargs_model={'lens_model_list': lens.lens_model_list, 'lens_redshift_list': lens.lens_redshift_list, 'source_light_model_list': ['SERSIC_ELLIPSE'], 'source_redshift_list': [config.z_gal], 'cosmo': lens.astropy_instance, 'z_source_convention': 2.5, 'z_source': 1.0})
                sim_i = SimAPI(numpix=64, kwargs_single_band=Euclid(band='VIS', coadd_years=6).kwargs_single_band(), kwargs_model={'lens_model_list': lens.lens_model_list, 'lens_redshift_list': lens.lens_redshift_list, 'source_light_model_list': ['SERSIC_ELLIPSE'], 'source_redshift_list': [config.z_gal], 'cosmo': lens.astropy_instance, 'z_source_convention': 2.5, 'z_source': 1.0})
                
                kwargs_numerics = {'point_source_supersampling_factor': 1}
                imSim_g = sim_g.image_model_class(kwargs_numerics)
                imSim_r = sim_r.image_model_class(kwargs_numerics)
                imSim_i = sim_i.image_model_class(kwargs_numerics)
                
                center_x, center_y = config.source_pos_x, config.source_pos_y
                kw_src_g = [{'magnitude': 22, 'R_sersic': 0.25, 'n_sersic': 1, 'e1': 0, 'e2': 0, 'center_x': center_x, 'center_y': center_y}]
                kw_src_r = [{'magnitude': 21, 'R_sersic': 0.25, 'n_sersic': 1, 'e1': 0, 'e2': 0, 'center_x': center_x, 'center_y': center_y}]
                kw_src_i = [{'magnitude': 20, 'R_sersic': 0.25, 'n_sersic': 1, 'e1': 0, 'e2': 0, 'center_x': center_x, 'center_y': center_y}]
                
                _, src_g, _ = sim_g.magnitude2amplitude(None, kw_src_g)
                _, src_r, _ = sim_r.magnitude2amplitude(None, kw_src_r)
                _, src_i, _ = sim_i.magnitude2amplitude(None, kw_src_i)
                
                img_g = imSim_g.image(lens.kwargs_lens_list, src_g, None)
                img_r = imSim_r.image(lens.kwargs_lens_list, src_r, None)
                img_i = imSim_i.image(lens.kwargs_lens_list, src_i, None)
                
                img_g += sim_g.noise_for_model(model=img_g)
                img_r += sim_r.noise_for_model(model=img_r)
                img_i += sim_i.noise_for_model(model=img_i)
                
                rgb_img = np.zeros((img_g.shape[0], img_g.shape[1], 3), dtype=float)
                rgb_img[:,:,0] = img_i
                rgb_img[:,:,1] = img_r
                rgb_img[:,:,2] = img_g
                image_data = rgb_img
                
            # Save output
            file_id = str(uuid.uuid4())
            npy_path = os.path.join(output_dir, f"{config.model_type}_{config.substructure}_{file_id}.npy")
            png_path = os.path.join(output_dir, f"{config.model_type}_{config.substructure}_{file_id}.png")
            np.save(npy_path, image_data)
            plt.figure(figsize=(5,5))
            plt.imshow(image_data, cmap='viridis')
            plt.colorbar()
            plt.title(f"{config.model_type} - {config.substructure}")
            plt.savefig(png_path)
            plt.close()
            
            generated_files.append({"npy_path": npy_path, "png_path": png_path})
            
        return {
            "status": "success",
            "message": f"Successfully generated {config.num_simulations} simulation(s).",
            "files": generated_files,
            "config_used": config.model_dump()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Simulation failed: {str(e)}",
            "details": "This error usually occurs due to invalid astrophysical parameters (e.g. invalid redshifts or mass ranges)."
        }

