# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'County.kmz_file'
        db.add_column(u'tigerline_county', 'kmz_file',
                      self.gf('smart_fields.models.fields.SmartFileField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'SubCounty.kmz_file'
        db.add_column(u'tigerline_subcounty', 'kmz_file',
                      self.gf('smart_fields.models.fields.SmartFileField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'State.kmz_file'
        db.add_column(u'tigerline_state', 'kmz_file',
                      self.gf('smart_fields.models.fields.SmartFileField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'County.kmz_file'
        db.delete_column(u'tigerline_county', 'kmz_file')

        # Deleting field 'SubCounty.kmz_file'
        db.delete_column(u'tigerline_subcounty', 'kmz_file')

        # Deleting field 'State.kmz_file'
        db.delete_column(u'tigerline_state', 'kmz_file')


    models = {
        u'tigerline.county': {
            'Meta': {'object_name': 'County'},
            'fips_55_class_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'fips_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'functional_status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'kmz_file': ('smart_fields.models.fields.SmartFileField', [], {'max_length': '100', 'null': 'True'}),
            'legal_statistical_description': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_and_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tigerline.State']", 'null': 'True'}),
            'state_fips_code': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'tigerline.state': {
            'Meta': {'ordering': "['name']", 'object_name': 'State'},
            'division': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fips_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.PositiveSmallIntegerField', [], {'primary_key': 'True'}),
            'kmz_file': ('smart_fields.models.fields.SmartFileField', [], {'max_length': '100', 'null': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'region': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'usps_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'})
        },
        u'tigerline.subcounty': {
            'Meta': {'object_name': 'SubCounty'},
            'county': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tigerline.County']", 'null': 'True'}),
            'county_fips_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'fips_55_class_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'fips_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'functional_status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'kmz_file': ('smart_fields.models.fields.SmartFileField', [], {'max_length': '100', 'null': 'True'}),
            'legal_statistical_description': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_and_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tigerline.State']", 'null': 'True'}),
            'state_fips_code': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['tigerline']