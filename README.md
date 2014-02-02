sinz
====

Sinz Is Not ZWA

Sinz is a set of scripts for continous integration of multiple interdependent packages.

Be aware that this is - and probably always will be - a work in progress.
The initial release is just the set of scripts we are currently using for the build workflows
of Zorp, the application level firewall suite, and Zenta, the metamodel aware architecture editor.

We follow the "Do Not Reinvent The Wheel" approach:
1. Sinz uses and depends on the already available tools for their already available functionality
2. Sinz do not require special preparation from the source packages,
    instead it uses the canonical interfaces of the canonical ways of building, but
3. Individual sinz functionalities depend on specific canonical ways of building, with the assumptions documented.
    For example some functionalities require the project to be a git repository, others require corret debian/changelog
4. Sinz relies on the configuration set in the way specific to the tools used, and provides the logic for the build.
    The rule of thum is the following: "If you would write anything in the CI tools with logic, you should update Sinz"

Workflows known by Sinz:

1. Cloud workflow
    Packages are in github, build and deployment with travis, github.io, launchpad and public osb
    Sins provides build and deployment scripts for the various cloud services.

2. Private workflow
    Packages are in private repositories, and build uses private jenkins and OBS instances.

