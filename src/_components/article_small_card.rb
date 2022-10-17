class ArticleSmallCard < BaseComponent
    renders_one :icon

    def initialize(article:, **opts)
        @article, @opts = article, opts
    end

    attr_reader :article, :opts
end