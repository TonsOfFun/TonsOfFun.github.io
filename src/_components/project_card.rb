class ProjectCard < BaseComponent
    def initialize(project:, project_type:, **opts)
        @project, @project_type, @opts = project, project_type, opts
    end

    attr_reader :project, :project_type, :opts
end