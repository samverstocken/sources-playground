# Imports
from pts.magic.core.frame import Frame
from pts.magic.core.image import Image
from pts.magic.sources.finder import SourceFinder
from pts.magic.catalog.extended import ExtendedSourceCatalog
from pts.magic.sources.extractor import SourceExtractor

name  = '1237678777941229794'
ra    = 0.00945
dec   = 5.28824
d25   = 0.42657951411792816
redshift = 0.1694



## Create the catalog
catalog = ExtendedSourceCatalog()

# Add the principal galaxy
# Arguments: name, ra, dec, z, galtype, alternative_names, distance, inclination, d25, major, minor, posangle, principal, companions, parent
# SET PRINCIPAL=TRUE FOR PRINCIPAL GALAXY
catalog.add_entry(name=name, ra=ra, dec=dec, z=redshift, galtype=None, alternative_names=None, distance=None, inclination=None, d25=d25, major=0.5*d25, minor=0.5*d25, posangle=0, principal=True, companions=None, parent=None)

# Catalog can be saved as follows:
#catalog.saveto(...)

## Create the instance
finder = SourceFinder()

## Configuration settings: can be adapted as preferred

# Multiprocessing is quite unstable
finder.config.nprocesses = 1

# Enable or disable certain features
finder.config.find_galaxies = True
finder.config.find_stars = True
finder.config.find_other_sources = True

# Give paths for extended and point source catalog files (if they have been created before; otherwise comment out)
#finder.config.extended_sources_catalog = ...
#finder.config.point_sources_catalog = ...

# Set the output directory
finder.config.output = 'output_find/'

# Set options for extended sources, point sources and other sources
# For extended source options: see 'definition' in pts.magic.config.find_extended.py
# For point source options: see 'definition' in pts.magic.config.find_point.py
# For other source options: see 'definition' in pts.magic.config.find_other.py
#finder.config.extended. .. = ...
#finder.config.point. ... = ...
#finder.config.other. ... = ...

## Add your image frame(s)
# Output path can be specified seperately for each frame
frame = Frame.from_file("testIm-i.fits")

#finder.add_frame(frame="J000002.00+051717.0_1237678777941229794-g.fits", name=name, output_path='output/')
#finder.add_frame(...)
#...

## Start the source finder:
# various kinds of input can be passed here:
# - frames: a FrameList instance
# - dataset: a DataSet instance
# - output_paths: a dictionary of output paths for each frame
# - star_finder_settings: different settings for each frame
# - ignore: ignore images (list of names)
# - ignore_stars: ignore stars for these images (list of names)
# - ignore_other_sources: ignore other sources for these images (list of names)
# - extended_source_catalog: object of ExtendedSourceCatalog class
# - point_source_catalog: object of PointSourceCatalog class
# CATALOGS ARE USED FOR ALL FRAMES -> IF CATALOG IS DIFFERENT FOR EACH IMAGE, ONLY ADD ONE FRAME TO THE FINDER AND RUN THIS SCRIPT FOR THE DIFFERENT IMAGES
finder.run(frames=dict([(name, frame)]), extended_source_catalog=catalog)

# Start source extraction
extractor = SourceExtractor()
extractor.config.input = 'output_find/'
extractor.config.output = 'output_extract/'

extractor.run(frame=frame, name=name)
