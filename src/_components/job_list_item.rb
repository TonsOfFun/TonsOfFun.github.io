class JobListItem < BaseComponent
    renders_one :icon

    def initialize(job:, **opts)
        @job, @opts = job, opts
    end

    attr_reader :job, :opts
end