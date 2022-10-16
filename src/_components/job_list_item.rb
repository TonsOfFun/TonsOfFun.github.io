class JobListItem < BaseComponent
    def initialize(job:, **opts)
        @job, @opts = job, opts
    end

    attr_reader :job, :opts
end