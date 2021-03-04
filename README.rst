============
RAD Pipeline
============


.. image:: https://img.shields.io/pypi/v/rad_pipeline.svg
        :target: https://pypi.python.org/pypi/rad_pipeline

.. image:: https://img.shields.io/travis/ahasha/rad_pipeline.svg
        :target: https://travis-ci.com/ahasha/rad_pipeline

.. image:: https://readthedocs.org/projects/rad-pipeline/badge/?version=latest
        :target: https://rad-pipeline.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




MassEnergize Renewable Actions Dataset Pipeline

* Free software: MIT license
* Documentation: https://rad-pipeline.readthedocs.io.

Raw Data Sources
=====================================

Electric Vehicles
-----------------

-  Source: Center for Sustainable Energy (2020). Massachusetts
   Department of Energy Resources Massachusetts Offers Rebates for
   Electric Vehicles, Rebate Statistics.
-  Retrieved 09/08/2020 from: https://mor-ev.org/program-statistics
-  Data last updated 08/21/2020. Data date range includes 06/19/2014 -
   08/15/2020.
-  Sectors: Residential.

Residential Air-source Heat Pumps (ASHP)
----------------------------------------

-  Source: Massachusetts Clean Energy Center (2020). Air Source Heat
   Pump Program - Residential Projects.
-  Retrieved 09/08/2020 from:
   http://files-cdn.masscec.com/ResidentialASHPProjectDatabase%2011.4.2019.xlsx
-  Data last updated 11/04/2019. Data date range includes 12/26/2014 -
   10/23/2019.
-  Sectors: Residential.

Ground-source Heat Pumps (GSHP)
-------------------------------

-  Source: Massachusetts Clean Energy Center (2020). Ground Source Heat
   Pump Program - Residential & Small-Scale Projects Database.
-  Retrieved 09/08/2020 from:
   http://files-cdn.masscec.com/get-clean-energy/govt-np/clean-heating-cooling/ResidentialandSmallScaleGSHPProjectDatabase.xlsx
-  Data last updated June 2020. Data date range includes 01/02/2015 -
   06/09/2020.
-  Sectors: Residential, Small Commercial.

Production Tracking System for Solar Photovoltaic Report (PV in PTS)
--------------------------------------------------------------------

-  Source: Massachusetts Clean Energy Center
-  According to a `September 2017 Department of Public Utilities
   Report <https://fileservice.eea.comacloud.net/FileService.Api/file/FileRoom/9174030>`__,
   “On a monthly basis, DOER and MassCEC compile data from the
   production tracking system to produce the MA PV Report, which is a
   publicly available document. The MA PV Report is available
   electronically at
   http://files.masscec.com/uploads/attachments/PVinPTSwebsite.xlsx.”
   However, the file at that URL does not seem to have been updated
   since November 2019. We analyze it here, but need to search for a
   source of ongoing updated data.
-  Sectors: Residential, Commercial, Institutional


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
