class JobListItem < BaseComponent
    def initialize(company:, **opts)
        @company, @opts = company, opts
    end

    attr_reader :company, :opts
end