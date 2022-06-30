import datetime
import hashlib
from itertools import chain
import json
from urllib import response
from flask import Flask,jsonify,request
#structuring blockchain
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(owner='owner',reg_no='001',prev_hash='0',proof=1)

    def create_block(self,owner,reg_no,proof,prev_hash):
        block={
                "owner":owner,
                "reg_no":reg_no,
                "timestamp":str(datetime.datetime.now()),
                "index":len(self.chain)+1,
                "proof":proof,
                "prev_hash":prev_hash
        }
        self.chain.append(block)
        return block

    def proof_of_work(self,prev_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_val=hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_val[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    def hash(self,block):
        encoded_block=json.dumps(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_idx=1
        while block_idx<len(chain):
            block=chain[block_idx]
            if block["prev_hash"]!=self.hash(previous_block):
                return False
            prev_proof=previous_block['proof']
            proof=block['proof']
            hash_val=hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_val[:4]!='0000':
                return False
            previous_block=block
            block_idx+=1
        return True
    
    def get_last_block(self):
        return self.chain[-1]

#creating web app

app = Flask(__name__)

blockchain=Blockchain()
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response={
        "chain":blockchain.chain,
        "length":len(blockchain.chain)
    }
    return jsonify(response),200

@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response={'message':'the ledger is valid'}
    else:
        response={'message':'the ledger is not valid'}

    return jsonify(response),200

@app.route('/mine_block', methods=['POST'])
def mine_block():
    values=request.get_json()
    required=['owner','reg_no']
    if not all(k in values for k in required):
        return 'missing values',400
    owner=values['owner']
    reg_no=values['reg_no']
    prev_block=blockchain.get_last_block()
    prev_proof=prev_block['proof']
    proof=blockchain.proof_of_work(prev_proof)
    prev_hash=blockchain.hash(prev_block)
    block= blockchain.create_block(owner,reg_no,proof,prev_hash)
    response={'message':'recod will be added to ledger'}

    return jsonify(response),200

app.run(host='0.0.0.0',port=8080,debug=True)

