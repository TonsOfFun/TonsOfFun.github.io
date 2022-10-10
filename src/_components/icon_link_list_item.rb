class IconLinkListItem < BaseComponent
    renders_one :icon

    def initialize(social:, **opts)
        @social, @opts = social, opts
    end

    attr_reader :social, :opts
end