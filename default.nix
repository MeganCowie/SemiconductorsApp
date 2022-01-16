# if you have Nix installed,
# this will provide a development environment for you via `nix-shell`
with import (fetchTarball https://releases.nixos.org/nixos/21.05/nixos-21.05.3761.93ca5ab64f7/nixexprs.tar.xz) {};
with pkgs.python38Packages;
let
  dash_bootstrap_components = buildPythonPackage rec {
      pname = "dash-bootstrap-components";
      version = "0.13.1";

      propagatedBuildInputs = [dash];
      src = fetchPypi {
        inherit pname version;
        sha256 = "02p77b4g8cn4g49a3kyam9sjqgjzcjsvzxqgrk0ml07cgg1pbb84";
      };

      doCheck = false;
  };

  dash_daq = buildPythonPackage rec {
      pname = "dash_daq";
      version = "0.5.0";

      propagatedBuildInputs = [dash];
      /* src = fetchTarball https://github.com/plotly/dash-daq/archive/v0.5.0.tar.gz; */
      src = fetchPypi {
        inherit pname version;
        sha256 = "0si5wjnl5sxy8fwm1lx82r32ahccnnyswi5w5xjqbf7pk5kmpn51";
      };

      doCheck = true;
  };

  dash-defer-js-import = buildPythonPackage rec {
      pname = "dash_defer_js_import";
      version = "0.0.2";

      propagatedBuildInputs = [dash];
      src = fetchPypi {
        inherit pname version;
        sha256 = "0jhyvwhp1i0dnivzhvwmsqwi9zbc2d4hgpymshxfsdb5sj9yygs0";
      };

      doCheck = false;
  };
in
rec {
  app = pkgs.stdenv.mkDerivation {
    name = "SemiconductorsApp";
    version = "1.0";
    src = ./.;
    installPhase = ''
      cp -R $src $out
    '';
  };

  app-bin = writeShellScriptBin "server" ''
    export PYTHONPATH="${app}:$PYTHONPATH"
    exec ${python-env}/bin/gunicorn app:server -w4
  '';

  python-env = pkgs.python3.buildEnv.override {
    extraLibs = [
      dash
      dash_bootstrap_components
      dash_daq
      dash-defer-js-import

      joblib
      scipy
      pandas
      flake8
      gunicorn
    ];
  };

  image = pkgs.dockerTools.streamLayeredImage {
    name = "semiconductorsapp";
    tag = "latest";
    config = {
      Cmd = [ "${python-env}/bin/gunicorn" "app:server" "-w4" ];
      WorkingDir = "${app}";
    };
  };
}
