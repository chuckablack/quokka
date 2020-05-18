def get_model_as_dict(model_obj):

    model_dict = dict()
    for k, v in model_obj.__dict__.items():

        if k.startswith("_"):
            continue

        if isinstance(v, list) or isinstance(v, dict):
            get_model_as_dict(v)
        else:
            model_dict[k] = v

    return model_dict
