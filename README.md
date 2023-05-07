# Just a random script for myself

## Installation

```
brew tap amachang/random-scripts
brew install --HEAD random-scripts
```

## Update

```
brew update
brew reinstall random-scripts
```

## Debug local formula

To check the behavior of Formula before `git commit`, we can do the following. I wish I knew a better way...

```
cp Formula/random-scripts.rb /usr/local/Homebrew/Library/Taps/amachang/homebrew-random-scripts/Formula/random-scripts.rb && brew reinstall random-script
```

