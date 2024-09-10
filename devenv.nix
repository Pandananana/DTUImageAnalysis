{ pkgs, lib, config, inputs, ... }:

{
  languages.python = {
    enable = true;
    version = "3.9";
    venv.enable = true;
    venv.requirements = ''
      scikit-image
      matplotlib
      pydicom
      jupyter 
      notebook
      ipykernel
    '';
    uv.enable = true;
  };
}
