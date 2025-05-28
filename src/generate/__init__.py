from abc import ABC, abstractmethod


class AbstractDependency(ABC):
    """
    TODO add label here
    """
    pass


class AbstractManifestGenerator(ABC):
    """
    TODO add dependencies related methods
    """

    @abstractmethod
    def gen():
        pass


class AbstractGenerationStrategy(ABC):

    @abstractmethod
    def load_dependency(self, label, artifact_def):
        """
        For the given label and artifact_def, returns a dependency instance.

        artifact_def is provided if the label is a source ref, for example,
        if the label is //projects/libs/cool_lib1 then the artifact_def
        is the parsed artifact file for projects/libs/cool_lib1.

        Args:
            label common.label.Label, the label for which to return a
            dependency (AbstractDependency)
            artifact_def crawl.buildpom.MavenArfifactDef for source labels,
            the artifact the label points to
        Returns:
            AbstractDependency instance
        """
        pass

    @abstractmethod
    def load_transitive_closure(self, dependency):
        """
        Given a dependency instance, returns the transitive closure of
        all dependencies this given one references.

        This method is only called for 3rd party dependencies (for ex jar
        dependencies).

        We could use bazel query to get the same information, but it is
        faster to parse the "pinned dependency file" once.
        """
        pass

    def new_generator(self, ctx):
        """
        Configures and returns a new manifest generator.
        """
        gen = self._init_generator__hook(ctx.artifact_def)
        gen.register_dependencies(ctx.direct_dependencies)
        gen.register_dependencies_transitive_closure__artifact(ctx.artifact_transitive_closure)
        gen.register_dependencies_transitive_closure__library(ctx.library_transitive_closure)
        return gen
        
    @abstractmethod
    def _init_generator__hook(self, artifact_def):
        """
        Returns a new AbstractManifestGenerator instance.

        Hook method, only meant to be implementation in subclasses.
        """
        pass
