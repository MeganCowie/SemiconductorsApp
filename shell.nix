# if you have Nix installed,
# this will provide a development environment for you via `nix-shell`
with import (fetchTarball https://releases.nixos.org/nixos/21.05/nixos-21.05.3761.93ca5ab64f7/nixexprs.tar.xz) {};
let
  pythonEnv = (import ./default.nix).python-env;
in
pkgs.mkShell {
  shellHook = ''
      # Here we have an opportunity to set environment variables!
    '';

  buildInputs = [
    pythonEnv
  ];
}
