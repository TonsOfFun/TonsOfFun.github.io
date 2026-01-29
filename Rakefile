require "bridgetown"

Bridgetown.load_tasks

# Run rake without specifying any command to execute a deploy build by default.
task default: :deploy

#
# Standard set of tasks, which you can customize if you wish:
#
desc "Build the Bridgetown site for deployment"
task :deploy => [:clean, "frontend:build"] do
  Bridgetown::Commands::Build.start
end

desc "Build the site in a test environment"
task :test do
  ENV["BRIDGETOWN_ENV"] = "test"
  Bridgetown::Commands::Build.start
end

desc "Runs the clean command"
task :clean do
  Bridgetown::Commands::Clean.start
end

namespace :frontend do
  desc "Build the frontend with esbuild for deployment"
  task :build do
    sh "touch frontend/styles/jit-refresh.css"
    sh "yarn run esbuild"
  end

  desc "Watch the frontend with esbuild during development"
  task :dev do
    sh "touch frontend/styles/jit-refresh.css"
    sh "yarn run esbuild-dev"
  rescue Interrupt
  end
end

#
# Add your own Rake tasks here! You can use `environment` as a prerequisite
# in order to write automations or other commands requiring a loaded site.
#

namespace :resume do
  desc "Generate PDF resume from the HTML resume page using Ferrum"
  task :pdf do
    require "ferrum"
    require "webrick"
    require "socket"

    output_dir = File.join(__dir__, "output")
    resume_html = File.join(output_dir, "resume", "index.html")
    pdf_output = File.join(output_dir, "resume.pdf")

    unless File.exist?(resume_html)
      puts "Error: Resume HTML not found at #{resume_html}"
      puts "Please run `bin/bridgetown build` first."
      exit 1
    end

    # Find an available port
    port = 4567
    begin
      server = TCPServer.new("127.0.0.1", port)
      server.close
    rescue Errno::EADDRINUSE
      port += 1
      retry
    end

    # Start a simple web server in a thread
    puts "Starting local server on port #{port}..."
    web_server = WEBrick::HTTPServer.new(
      Port: port,
      DocumentRoot: output_dir,
      Logger: WEBrick::Log.new("/dev/null"),
      AccessLog: []
    )

    server_thread = Thread.new { web_server.start }

    # Give server time to start
    sleep 0.5

    puts "Generating PDF from http://localhost:#{port}/resume/..."

    browser = Ferrum::Browser.new(
      headless: true,
      timeout: 60,
      window_size: [1200, 1600],
      browser_options: {
        "no-sandbox": nil,
        "disable-gpu": nil
      }
    )

    begin
      browser.go_to("http://localhost:#{port}/resume/")

      # Wait for CSS and fonts to load
      sleep 2

      # Wait for network to be idle (no pending requests)
      browser.network.wait_for_idle

      browser.pdf(
        path: pdf_output,
        format: :letter,
        print_background: true,
        landscape: false
      )

      puts "PDF generated successfully: #{pdf_output}"
    ensure
      browser.quit
      web_server.shutdown
      server_thread.join(5)
    end
  end
end

desc "Build site and generate resume PDF"
task :build_with_resume => [:deploy, "resume:pdf"]
