# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals


# Pipeline
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
PIPELINE_CSS = {
    'bootstrap': {
        'source_filenames': [
            'lib/bootstrap/less/bootstrap.less',
        ],
        'output_filename': 'lib/bootstrap/bootstrap.css',
        'extra_context': {
            'media': 'screen',
        },
    },
    'onetime': {
        'source_filenames': [
            'onetime/less/onetime.less',
        ],
        'output_filename': 'onetime/css/onetime.css',
        'extra_context': {
            'media': 'screen',
        },
    },
    'login': {
        'source_filenames': [
            'account/less/login.less',
        ],
        'output_filename': 'account/css/login.css',
        'extra_context': {
            'media': 'screen',
        },
    },
    'errors': {
        'source_filenames': [
            'errors/less/errors.less',
        ],
        'output_filename': 'errors/css/errors.css',
        'extra_context': {
            'media': 'screen',
        },
    },
}
PIPELINE_JS = {
    'onetime': {
        'source_filenames': [
            'lib/angular/angular.min.js',
            'lib/angular/angular-resource.min.js',
            'lib/angular/angular-ui-router.min.js',
            'onetime/js/app.js',
            'onetime/js/controllers/message.js',
            'onetime/js/controllers/message-create.js',
            'onetime/js/controllers/message-created.js',
            'onetime/js/directives/password.js',
            'onetime/js/directives/select-on-focus.js',
            'onetime/js/directives/textheight.js',
            'onetime/js/filters/is-empty.js',
            'onetime/js/services/crypto.js',
            'onetime/js/services/entropy.js',
            'onetime/js/services/otsecret.js',
            'onetime/js/services/state.js',
            'lib/forge/forge.min.js',
        ],
        'output_filename': 'onetime/js/onetime.js'
    },
    'bootstrap': {
        'source_filenames': [
            'lib/jquery/jquery.min.js',
            'lib/bootstrap/js/affix.js',
            'lib/bootstrap/js/alert.js',
            'lib/bootstrap/js/button.js',
            'lib/bootstrap/js/carousel.js',
            'lib/bootstrap/js/collapse.js',
            'lib/bootstrap/js/dropdown.js',
            'lib/bootstrap/js/modal.js',
            'lib/bootstrap/js/popover.js',
            'lib/bootstrap/js/scrollspy.js',
            'lib/bootstrap/js/tab.js',
            'lib/bootstrap/js/tooltip.js',
            'lib/bootstrap/js/transition.js',
        ],
        'output_filename': 'lib/bootstrap/bootstrap.js',
    },
    'ie': {
        'source_filenames': [
            'lib/html5shiv/html5shiv.js',
            'lib/respond/respond.js',
        ],
        'output_filename': 'lib/ie.js',
    },
}
