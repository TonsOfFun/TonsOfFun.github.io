class ProjectCard < BaseComponent
    def initialize(project:, **opts)
        @project, @opts = project, opts
    end

    attr_reader :project, :opts
end