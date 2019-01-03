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

Install requests lambda dependency (in lambda repository)
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

## Home Assistant configuration

Check perhaps first that your [Home Assistant Rest API] if working, you can check this with a simple curl command (see the documentation)

As this is using the "smart home" alexa component (Home Assistant have also a cloud Alexa integration, this one is not the cloud one), you need to enter a alexa/smart_home section in your HA configuration (see again [Home Assistant Alexa] Smart Home part):

```yaml
alexa:
  smart_home:
    filter:
      include_entities:
        - ...
        - ...
      include_domains:
        ...
      exclude_entities:
        ...
    entity_config:
      ...
```

Restart Home Assistant, you can chek if the endpoint ``` http://<your ha ip>:<port>/api/alexa/smart_home```  is now up (=> https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/alexa/smart_home.py#L60)

Be careful with HA configuration, ```include_domains``` include all devices of the domain by default, I'm not using it and add manually one to one devices I want to control with Alexa.

[Home Assistant Alexa]: https://www.home-assistant.io/components/alexa/#smart-home
[haaska]: https://github.com/mike-grant/haaska
[Alexicz]: https://github.com/rimram31/dz_smarthome
[Home Assistant Rest API]: https://developers.home-assistant.io/docs/en/external_api_rest.html
