class AppearanceCard < BaseComponent
    renders_one :icon

    def initialize(appearance:, **opts)
        @appearance, @opts = appearance, opts
    end

    attr_reader :appearance, :opts
end