class RoleCard < BaseComponent
    def initialize(role:, company:, **opts)
        @role, @company, @opts = role, company, opts
    end

    attr_reader :role, :company, :opts
end