class TagList < BaseComponent
  def initialize(tags: [], tag_styles: (Bridgetown::Current&.site || Bridgetown::Site.new).data.tag_styles)
    @tags, @tag_styles = (tags || []), tag_styles
  end

  attr_reader :tags, :tag_styles
end