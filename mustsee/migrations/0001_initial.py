# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attraction'
        db.create_table('mustsee_attraction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('mustsee', ['Attraction'])

        # Adding model 'UserRank'
        db.create_table('mustsee_userrank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attraction', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ranks', to=orm['mustsee.Attraction'])),
            ('session_uuid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(default=-1, null=True)),
        ))
        db.send_create_signal('mustsee', ['UserRank'])

        # Adding unique constraint on 'UserRank', fields ['attraction', 'session_uuid']
        db.create_unique('mustsee_userrank', ['attraction_id', 'session_uuid'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserRank', fields ['attraction', 'session_uuid']
        db.delete_unique('mustsee_userrank', ['attraction_id', 'session_uuid'])

        # Deleting model 'Attraction'
        db.delete_table('mustsee_attraction')

        # Deleting model 'UserRank'
        db.delete_table('mustsee_userrank')


    models = {
        'mustsee.attraction': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Attraction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'mustsee.userrank': {
            'Meta': {'unique_together': "(('attraction', 'session_uuid'),)", 'object_name': 'UserRank'},
            'attraction': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ranks'", 'to': "orm['mustsee.Attraction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True'}),
            'session_uuid': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['mustsee']