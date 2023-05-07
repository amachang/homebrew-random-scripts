require "language/node"

class RandomScripts < Formula
  include Language::Python::Virtualenv

  head "https://github.com/amachang/homebrew-random-scripts.git", :branch => "main"
  depends_on "python@3.9"
  depends_on "node@18"
  depends_on "pixman"
  depends_on "cairo"
  depends_on "pango"

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

    export_files = [
      "hello_python",
      "rename_with_dir",
      "major_image_res",
      "hello_node",
      "top_disk_io",
    ]
    export_files.each do |file|
      bin.install_symlink "#{libexec}/bin/#{file}"
    end
  end
end
