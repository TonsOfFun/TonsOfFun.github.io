module Filters
  def github_edit_url(resource)
  "https://github.com/#{site.metadata.repo}/blob/main/src/#{resource.relative_path}"
  end
end

Bridgetown::RubyTemplateView::Helpers.include Filters