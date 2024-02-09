class Synapse < Formula
    desc "Use synapse to manage Neuralib packages"
    homepage "https://alessiofanelli.com/synapse"
    url "https://raw.githubusercontent.com/FanaHOVA/homebrew-synapse/main/synapse"
    sha256 "f5e9a58690fd5f225e6cc7e34ffa1a28f784d3a3fba215847270964d769e8139"
    version "0.0.5"

    depends_on "jq"
  
    def install
      bin.install "synapse"
    end
  end
