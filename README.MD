# Alexa Smart Home Proxy skill

## Presentation

This repo contains python (3) lambda code to relay Lambda Smart Home Alexa API calls to a given local endpoint. Thanks to [haaska] code.

I'm using it for Home Assistant Alexa skill (See [Home Assistant Alexa] Smart Home part). I'm also using it to debug [Alexicz] (proxy Smart Home API calls from lambda to a local proxy server)

I've also put here (very) basic scripts I'm using to package and update AWS lambda (require aws cli to be installed)

## Installing the skill

Same as other skill, see for example [Alexicz] documentation. You have to create an Amazon Developer Account, an Amazon Web Service account to host the Alexa lambda (this one) with a first version of the lambda zip package (Python 3.6 lambda engine)

```sh
git clone git@github.com:rimram31/alexa_smarthome.git
cd alexa_smarthome
```

To create your package, zip file, you must adjust the expected configuration file ```config.json```: your url endpoint, home assistant api password if defined ...
```sh
cp config-template.json config.json
vi config.json
```

## Packaging/updating the lambda

Install requets lambda dependency (in lambda repository)
```sh
pip3 install requests  --target .
```

Build the lambda zip file
```sh
./build_lambda
```

Update AWS lambda function
```sh
./update_lambda
```

Note: If you change lambda code and this will change dependencies, I'm using a virtualenv to be able to check them and install all in local repo with ```--target``` pip option.

[Home Assistant Alexa]: https://www.home-assistant.io/components/alexa/
[haaska]: https://github.com/mike-grant/haaska
[Alexicz]: https://github.com/rimram31/dz_smarthome
