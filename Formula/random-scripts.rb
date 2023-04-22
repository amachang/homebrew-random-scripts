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
    venv = virtualenv_create(libexec)
    venv.pip_install buildpath/"python"

    chdir "node" do
      system "npm", "install", *Language::Node.std_npm_install_args(libexec)
    end
    bin.install_symlink Dir["#{libexec}/bin/hello_node"]
    bin.install_symlink Dir["#{libexec}/bin/hello_python"]
  end
end
