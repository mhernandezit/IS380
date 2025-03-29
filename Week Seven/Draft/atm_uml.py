from graphviz import Digraph

dot = Digraph('ATM_UML', filename='atm_uml.gv', format='png')
dot.attr(rankdir='TB', splines='ortho')  # Top-to-bottom layout with orthogonal edges

# Define nodes
dot.node('start', '', shape='circle', style='filled', fillcolor='black')
dot.node('insert_card', 'Insert Card', shape='box')
dot.node('enter_pin', 'Enter PIN', shape='box')
dot.node('select_option', 'Select Option:\nCheck Balance / Withdraw / Exit', shape='box')
dot.node('validate_card', 'Validate Card', shape='box')
dot.node('cash_check', 'ATM Cash Available?', shape='diamond')
dot.node('atm_out', 'ATM Out of Money', shape='box', style='filled', fillcolor='red')
dot.node('secure_conn', 'Establish Secure Connection\n& Transmit Card/PIN', shape='box')
dot.node('pin_verify', 'PIN Verification &\nReturn Balance', shape='box')
dot.node('invalid_pin', 'Error: Invalid PIN\nEject Card', shape='box', style='filled', fillcolor='red')
dot.node('store_balance', 'Store Bank Balance', shape='box')
dot.node('option_decision', 'Option Decision', shape='diamond')
dot.node('display_balance', 'Display Balance', shape='box')
dot.node('withdraw_amount', 'Enter Withdrawal Amount', shape='box')
dot.node('process_withdraw', 'Process Bank Withdrawal', shape='box')
dot.node('balance_check', 'Is Requested Amount ≤ Available Balance?', shape='diamond')
dot.node('withdraw_error', 'Error: Insufficient Balance\nEject Card', shape='box', style='filled', fillcolor='red')
dot.node('verify_atm_cash', 'Verify Sufficient ATM Cash', shape='diamond')
dot.node('deduct_amount', 'Deduct Amount', shape='box')
dot.node('dispense_cash', 'Dispense Cash', shape='box')
dot.node('eject_card', 'Eject Card', shape='box')
dot.node('end', '', shape='circle', style='filled', fillcolor='black')

# Define edges for the core flow

# Start to Actor actions
dot.edge('start', 'insert_card')
dot.edge('insert_card', 'enter_pin')
dot.edge('enter_pin', 'select_option')

# From Option Selection:
# If Exit, go directly to Eject Card.
dot.edge('select_option', 'eject_card', label='Exit', constraint='false')
# Otherwise, continue with transaction.
dot.edge('select_option', 'validate_card', label='Check Balance/Withdraw')

# Card validation and cash check
dot.edge('validate_card', 'cash_check')
dot.edge('cash_check', 'secure_conn', label='Yes')
dot.edge('cash_check', 'atm_out', label='No')
dot.edge('atm_out', 'eject_card')

# Secure connection to Bank for PIN verification and balance retrieval
dot.edge('secure_conn', 'pin_verify')
# On successful PIN verification, store the balance
dot.edge('pin_verify', 'store_balance', label='Valid')
# On PIN failure, go to invalid PIN error
dot.edge('pin_verify', 'invalid_pin', label='Invalid')
dot.edge('invalid_pin', 'eject_card')

# Decision after storing balance: show balance or withdraw money
dot.edge('store_balance', 'option_decision')
dot.edge('option_decision', 'display_balance', label='Show Balance')
dot.edge('display_balance', 'eject_card')
dot.edge('option_decision', 'withdraw_amount', label='Withdraw')

# Withdrawal flow
dot.edge('withdraw_amount', 'process_withdraw')
# Check if the requested withdrawal amount is less than or equal to the available balance
dot.edge('process_withdraw', 'balance_check')
dot.edge('balance_check', 'verify_atm_cash', label='Yes')
dot.edge('balance_check', 'withdraw_error', label='No')
dot.edge('withdraw_error', 'eject_card')
# Verify if the ATM has enough cash physically
dot.edge('verify_atm_cash', 'deduct_amount', label='Sufficient')
dot.edge('verify_atm_cash', 'atm_out', label='Insufficient')
dot.edge('deduct_amount', 'dispense_cash')
dot.edge('dispense_cash', 'eject_card')

# Finish process
dot.edge('eject_card', 'end')

# Render the diagram and view the result (this creates atm_uml.gv.png)
dot.render(view=True)
