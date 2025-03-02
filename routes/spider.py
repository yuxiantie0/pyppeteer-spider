import asyncio
import logging
import json
from flask import Blueprint, request, jsonify
from utils.spider import Spider

bp = Blueprint('spider', __name__)

# API: 获取pyppeteer处理后的网站内容
@bp.route('/fetch', methods=['POST'])
def fetch():
    try:
        reqs = request.get_json()
        url = reqs.get('url')
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'}), 400

        logging.info("request:" + json.dumps(reqs, ensure_ascii=False, indent=2))
        
        content = asyncio.run(Spider.fetch_page(
            url=url,
            cookies=reqs.get('cookie'),
            proxy=reqs.get('proxy'),
            user_agent=reqs.get('ua')
        ))
        
        return jsonify({
            'status': 'success',
            'data': content
        })
        
    except Exception as e:
        logging.error(f"Error in fetch route: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 