// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract FerroFy_INRf is IERC20 {
    address public constant FERROFY_OWNER = 0x91b2Aef20c29d87d8dcc48191b30FbC1562aAaF0;

    string public constant name = "FerroFy Indian Rupee";
    string public constant symbol = "INRf";
    uint8 public constant decimals = 2;

    uint256 public constant INITIAL_SUPPLY = 1_000_000_000 * 10 ** uint256(decimals);

    uint256 private _totalSupply;
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    mapping(address => bool) public minters;

    event MinterUpdated(address indexed account, bool allowed);
    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == FERROFY_OWNER, "Only FerroFy owner");
        _;
    }

    modifier onlyOwnerOrMinter() {
        require(msg.sender == FERROFY_OWNER || minters[msg.sender], "Only owner or minter");
        _;
    }

    constructor() {
        require(msg.sender == FERROFY_OWNER, "Deploy from FerroFy owner");
        minters[FERROFY_OWNER] = true;
        emit MinterUpdated(FERROFY_OWNER, true);
        _mint(FERROFY_OWNER, INITIAL_SUPPLY);
        emit Mint(FERROFY_OWNER, INITIAL_SUPPLY);
    }

    function owner() external pure returns (address) {
        return FERROFY_OWNER;
    }

    function setMinter(address account, bool allowed) external onlyOwner {
        require(account != address(0), "Invalid minter");
        minters[account] = allowed;
        emit MinterUpdated(account, allowed);
    }

    function totalSupply() external view override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view override returns (uint256) {
        return _balances[account];
    }

    function allowance(address tokenOwner, address spender) external view override returns (uint256) {
        return _allowances[tokenOwner][spender];
    }

    function transfer(address to, uint256 amount) external override returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external override returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external override returns (bool) {
        uint256 currentAllowance = _allowances[from][msg.sender];
        if (currentAllowance != type(uint256).max) {
            require(currentAllowance >= amount, "ERC20: low allowance");
            unchecked {
                _approve(from, msg.sender, currentAllowance - amount);
            }
        }
        _transfer(from, to, amount);
        return true;
    }

    function mint(address to, uint256 amount) external onlyOwnerOrMinter {
        require(amount > 0, "Amount must be greater than zero");
        _mint(to, amount);
        emit Mint(to, amount);
    }

    function burn(address from, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than zero");
        _burn(from, amount);
        emit Burn(from, amount);
    }

    function _transfer(address from, address to, uint256 amount) private {
        require(from != address(0), "ERC20: transfer from zero");
        require(to != address(0), "ERC20: transfer to zero");
        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "ERC20: low balance");
        unchecked {
            _balances[from] = fromBalance - amount;
        }
        _balances[to] += amount;
        emit Transfer(from, to, amount);
    }

    function _approve(address tokenOwner, address spender, uint256 amount) private {
        require(tokenOwner != address(0), "ERC20: approve from zero");
        require(spender != address(0), "ERC20: approve to zero");
        _allowances[tokenOwner][spender] = amount;
        emit Approval(tokenOwner, spender, amount);
    }

    function _mint(address to, uint256 amount) private {
        require(to != address(0), "ERC20: mint to zero");
        _totalSupply += amount;
        _balances[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    function _burn(address from, uint256 amount) private {
        require(from != address(0), "ERC20: burn from zero");
        uint256 fromBalance = _balances[from];
        require(fromBalance >= amount, "ERC20: low balance");
        unchecked {
            _balances[from] = fromBalance - amount;
        }
        _totalSupply -= amount;
        emit Transfer(from, address(0), amount);
    }
}
