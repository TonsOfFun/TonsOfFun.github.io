class Shared::Header < Bridgetown::Component
    def initialize(metadata:, resource:, data:)
        @metadata, @resource, @data = metadata, resource, data
    end
end
  