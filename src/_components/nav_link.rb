class NavLink < BaseComponent
    renders_one :icon

    def initialize(link:, resource:, **opts)
        @link, @resource, @opts = link, resource, opts
    end

    attr_reader :link, :resource, :opts
end