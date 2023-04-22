class RandomScripts < Formula
  include Language::Python::Virtualenv

  head "https://github.com/amachang/homebrew-random-scripts.git", :branch => "main"
  depends_on "python@3.8"
  depends_on "node@18"

  def install
    venv = virtualenv_create(libexec, "python@3.8")
    venv.pip_insatll_and_link buildpath/"python"

    system "npm", "install", buildpath/"node", *Language::Node.std_npm_install_args(libexec)
    bin.install_symlink Dir["#{libexec}/bin/*"]
  end
end
