require "language/node"

class RandomScripts < Formula
  include Language::Python::Virtualenv

  head "https://github.com/amachang/homebrew-random-scripts.git", :branch => "main"
  depends_on "python@3.9"
  depends_on "node@18"
  depends_on "pixman"
  depends_on "cairo"
  depends_on "pango"
  depends_on "rust"
  depends_on "ffmpeg"

  def install
    venv_root = virtualenv_create(libexec).instance_variable_get("@venv_root")

    chdir "python" do
      system venv_root/"bin/pip", "install", ".", "-v", "--ignore-installed"
    end

    chdir "node" do
      system "npm", "install", *Language::Node.std_npm_install_args(libexec)
    end

    chdir "dtrace" do
      Dir.glob("*.d").each do |filename|
        exec_filename = File.basename(filename, ".d")
        (libexec/"bin").install filename => exec_filename
        chmod 0755, libexec/"bin/#{exec_filename}"
      end
    end

    chdir "rust" do
      system "git", "submodule", "init"
      system "git", "submodule", "update"
      Dir.glob("*").each do |projectname|
        chdir projectname do
          system "cargo", "build", "--release", "--bin", projectname
          (libexec/"bin").install "target/release/#{projectname}" => projectname
        end
      end
    end

    export_files = [
      "hello_python",
      "make_app",
      "rename_with_dir",
      "major_image_res",
      "hello_node",
      "top_disk_io",
      "drop_duplicate_files",
      "fq",
      "rename_video_files",
      "gofile",
      "rmjunk",
    ]
    export_files.each do |file|
      bin.install_symlink "#{libexec}/bin/#{file}"
    end
  end
end
