from flask import Blueprint, session, request, jsonify

syncs = Blueprint('syncs', __name__)

@syncs.route('/api/syncs/mine')
def get_sync():
  return jsonify({
    'status': 'syncing',
    'synced_calendars': [
      'jon@itso.io',
      'lucas@itso.io'
    ]
  })


@syncs.route('/api/syncs/mine', methods=['POST'])
def configure_sync():
  return jsonify({
    'status': 'syncing',
    'synced_calendars': [
      'jon@itso.io',
      'lucas@itso.io'
    ]
  })
