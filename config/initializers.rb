Bridgetown.configure do |config|
  require "bridgetown-cloudinary"
  require "bridgetown-svg-inliner"
  require "bridgetown-view-component"
  
  init :"bridgetown-cloudinary" do
    cloud_name "tonsoffun"
  end
end