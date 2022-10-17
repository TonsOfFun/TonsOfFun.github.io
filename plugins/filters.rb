module Filters
  def github_edit_url(resource)
  "https://github.com/#{site.metadata.source_url}/blob/main/src/#{resource.relative_path}"
  end
end

Bridgetown::RubyTemplateView::Helpers.include Filters