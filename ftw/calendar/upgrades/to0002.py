# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging


def clean_registries(context):
    """Performs the profile update

    Clean the resources removed from the skins folder
    """
    logger = logging.getLogger('ftw.calendar')

    unwanted_css = (
        'ftwcalendar.css',
        'fullcalendar.css',
    )
    css = getToolByName(context, 'portal_css')
    map(css.unregisterResource, unwanted_css)
    logger.info("portal_css is clean")

    unwanted_js = (
        'fullcalendar.min.js',
    )
    js = getToolByName(context, 'portal_javascripts')
    map(js.unregisterResource, unwanted_js)
    logger.info("portal_javascript is clean")

    skins = getToolByName(context, 'portal_skins')
    selections = skins._getSelections()
    unwanted_layers = (
        'ftwcalendar',
    )
    for key in selections:
        value = selections[key]
        layers = value.split(',')
        selections[key] = ','.join([
            layer for layer in layers if layer not in unwanted_layers
        ])
    logger.info("portal_skins is clean")
