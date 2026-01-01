"""
Mining Dashboard - Real-time monitoring and statistics
"""

import asyncio
import logging
from typing import Dict, List
from datetime import datetime, timedelta
import sys

logger = logging.getLogger(__name__)


# ANSI Color codes for terminal styling
class Colors:
    """Sci-fi themed color palette"""
    RESET = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Sci-fi theme colors
    NEON_GREEN = '\033[38;5;46m'
    NEON_CYAN = '\033[38;5;51m'
    NEON_PURPLE = '\033[38;5;165m'
    ELECTRIC_BLUE = '\033[38;5;39m'


class Dashboard:
    """Real-time mining dashboard with sci-fi aesthetics"""
    
    def __init__(self):
        self.is_running = False
        self.start_time = None
        self.stats_history = []
        self.frame_count = 0
        
    def _clear_screen(self):
        """Clear terminal screen"""
        print('\033[2J\033[H', end='')
    
    async def start(self):
        """Start the dashboard"""
        self.is_running = True
        self.start_time = datetime.now()
        logger.info("Dashboard started")
        asyncio.create_task(self._print_stats_loop())
    
    async def update_stats(self, workers: List[Dict], hashrate: float, shares: Dict):
        """Update dashboard statistics"""
        stats = {
            'workers': workers,
            'total_hashrate': hashrate,
            'shares': shares
        }
        self.stats_history.append(stats)
        
        # Keep only last 100 stats entries
        if len(self.stats_history) > 100:
            self.stats_history = self.stats_history[-100:]
    
    def _print_header(self):
        """Print sci-fi styled header with ASCII art"""
        c = Colors
        
        header = f"""
{c.NEON_CYAN}{c.BOLD}╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   {c.NEON_PURPLE}██████╗ ██╗████████╗ ██████╗ ██████╗ ██╗███╗   ██╗                    {c.NEON_CYAN}║
║   {c.NEON_PURPLE}██╔══██╗██║╚══██╔══╝██╔════╝██╔═══██╗██║████╗  ██║                    {c.NEON_CYAN}║
║   {c.NEON_PURPLE}██████╔╝██║   ██║   ██║     ██║   ██║██║██╔██╗ ██║                    {c.NEON_CYAN}║
║   {c.NEON_PURPLE}██╔══██╗██║   ██║   ██║     ██║   ██║██║██║╚██╗██║                    {c.NEON_CYAN}║
║   {c.NEON_PURPLE}██████╔╝██║   ██║   ╚██████╗╚██████╔╝██║██║ ╚████║                    {c.NEON_CYAN}║
║   {c.NEON_PURPLE}╚═════╝ ╚═╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝                    {c.NEON_CYAN}║
║                                                                           ║
║              {c.NEON_GREEN}M I N I N G   C O N T R O L   S Y S T E M{c.NEON_CYAN}                ║
║                      {c.DIM}[ Distributed Hash Protocol ]{c.RESET}{c.NEON_CYAN}                  ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝{c.RESET}
"""
        print(header)
    
    def _print_system_status(self, uptime: timedelta):
        """Print system status bar"""
        c = Colors
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        status_bar = f"""{c.ELECTRIC_BLUE}┌─────────────────────────────────────────────────────────────────────────┐
│ {c.BOLD}SYSTEM STATUS{c.RESET}{c.ELECTRIC_BLUE}                                                            │
│ {c.GREEN}●{c.RESET} UPTIME: {c.CYAN}{hours:02d}h {minutes:02d}m {seconds:02d}s{c.ELECTRIC_BLUE}                        FRAME: {c.YELLOW}{self.frame_count:05d}{c.ELECTRIC_BLUE}    │
└─────────────────────────────────────────────────────────────────────────┘{c.RESET}
"""
        print(status_bar)
    
    def _print_workers_table(self, workers: List[Dict], group_by_bank: bool = True):
        """Print worker status table with colors, optionally grouped by bank"""
        c = Colors
        
        if group_by_bank and workers:
            # Group workers by bank
            banks: Dict[str, List[Dict]] = {}
            for worker in workers:
                bank_name = worker.get('bank_name', 'Unknown')
                if bank_name not in banks:
                    banks[bank_name] = []
                banks[bank_name].append(worker)
            
            # Print each bank separately
            for bank_name, bank_workers in banks.items():
                self._print_bank_table(bank_name, bank_workers)
                print()  # Spacing between banks
        else:
            # Print all workers in one table
            self._print_single_worker_table(workers)
    
    def _print_bank_table(self, bank_name: str, workers: List[Dict]):
        """Print a table for a single bank"""
        c = Colors
        
        # Calculate bank stats
        active_count = sum(1 for w in workers if w['connected'])
        total_hashrate = sum(w['hashrate'] for w in workers if w['connected'])
        
        print(f"{c.NEON_PURPLE}┌─────────────────────────────────────────────────────────────────────────┐")
        print(f"│ {c.BOLD}{bank_name} - {active_count}/{len(workers)} ACTIVE{c.RESET}{c.NEON_PURPLE}    HASHRATE: {c.CYAN}{total_hashrate:>7.2f} H/s{c.NEON_PURPLE}               │")
        print(f"├────┬────────────────┬─────────────┬────────────────┬────────┬──────────┤")
        print(f"│{c.BOLD} ID │ PORT           │ STATUS      │ HASHRATE       │ SHARES │ ERRORS{c.RESET}{c.NEON_PURPLE}   │")
        print(f"├────┼────────────────┼─────────────┼────────────────┼────────┼──────────┤{c.RESET}")
        
        for worker in workers:
            w_id = f"{worker['id']:02d}"
            port = worker['port'][-12:] if len(worker['port']) > 12 else worker['port']
            
            if worker['connected']:
                status = f"{c.GREEN}● ONLINE{c.RESET}  "
                hashrate_color = c.CYAN if worker['hashrate'] > 50 else c.YELLOW
                hashrate = f"{hashrate_color}{worker['hashrate']:>6.2f} H/s{c.RESET}"
            else:
                status = f"{c.RED}○ OFFLINE{c.RESET} "
                hashrate = f"{c.DIM}  ---  H/s{c.RESET}"
            
            error_color = c.RED if worker['errors'] > 0 else c.GREEN
            
            print(f"{c.NEON_PURPLE}│{c.RESET} {c.BOLD}{w_id}{c.RESET} {c.NEON_PURPLE}│{c.RESET} {port:<14} {c.NEON_PURPLE}│{c.RESET} {status} {c.NEON_PURPLE}│{c.RESET} {hashrate:>22} {c.NEON_PURPLE}│{c.RESET} {worker['shares']:>6} {c.NEON_PURPLE}│{c.RESET} {error_color}{worker['errors']:>8}{c.RESET} {c.NEON_PURPLE}│{c.RESET}")
        
        print(f"{c.NEON_PURPLE}└────┴────────────────┴─────────────┴────────────────┴────────┴──────────┘{c.RESET}")
    
    def _print_single_worker_table(self, workers: List[Dict]):
        """Print all workers in a single table (legacy format)"""
        c = Colors
        
        print(f"{c.NEON_GREEN}┌─────────────────────────────────────────────────────────────────────────┐")
        print(f"│ {c.BOLD}MINING NODES STATUS{c.RESET}{c.NEON_GREEN}                                                    │")
        print(f"├────┬────────────────┬─────────────┬────────────────┬────────┬──────────┤")
        print(f"│{c.BOLD} ID │ PORT           │ STATUS      │ HASHRATE       │ SHARES │ ERRORS{c.RESET}{c.NEON_GREEN}   │")
        print(f"├────┼────────────────┼─────────────┼────────────────┼────────┼──────────┤{c.RESET}")
        
        for worker in workers:
            w_id = f"{worker['id']:02d}"
            port = worker['port'][-12:] if len(worker['port']) > 12 else worker['port']
            
            if worker['connected']:
                status = f"{c.GREEN}● ONLINE{c.RESET}  "
                hashrate_color = c.CYAN if worker['hashrate'] > 50 else c.YELLOW
                hashrate = f"{hashrate_color}{worker['hashrate']:>6.2f} H/s{c.RESET}"
            else:
                status = f"{c.RED}○ OFFLINE{c.RESET} "
                hashrate = f"{c.DIM}  ---  H/s{c.RESET}"
            
            error_color = c.RED if worker['errors'] > 0 else c.GREEN
            
            print(f"{c.NEON_GREEN}│{c.RESET} {c.BOLD}{w_id}{c.RESET} {c.NEON_GREEN}│{c.RESET} {port:<14} {c.NEON_GREEN}│{c.RESET} {status} {c.NEON_GREEN}│{c.RESET} {hashrate:>22} {c.NEON_GREEN}│{c.RESET} {worker['shares']:>6} {c.NEON_GREEN}│{c.RESET} {error_color}{worker['errors']:>8}{c.RESET} {c.NEON_GREEN}│{c.RESET}")
        
        print(f"{c.NEON_GREEN}└────┴────────────────┴─────────────┴────────────────┴────────┴──────────┘{c.RESET}")
    
    def _print_statistics_panel(self, stats: Dict):
        """Print overall statistics panel"""
        c = Colors
        shares = stats['shares']
        hashrate = stats['total_hashrate']
        
        # Determine hashrate display color
        if hashrate >= 250:
            hr_color = c.NEON_GREEN
            hr_status = "OPTIMAL"
        elif hashrate >= 150:
            hr_color = c.CYAN
            hr_status = "NOMINAL"
        else:
            hr_color = c.YELLOW
            hr_status = "SUBOPTIMAL"
        
        # Calculate acceptance rate color
        acc_rate = shares['acceptance_rate']
        if acc_rate >= 95:
            acc_color = c.GREEN
        elif acc_rate >= 80:
            acc_color = c.YELLOW
        else:
            acc_color = c.RED
        
        panel = f"""
{c.NEON_PURPLE}┌─────────────────────────────────────────────────────────────────────────┐
│ {c.BOLD}NETWORK STATISTICS{c.RESET}{c.NEON_PURPLE}                                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  {c.BOLD}TOTAL HASHRATE:{c.RESET}    {hr_color}{hashrate:>7.2f} H/s{c.RESET}                  [{c.BOLD}{hr_status}{c.RESET}]       │
│                                                                         │
│  {c.BOLD}SHARES SUBMITTED:{c.RESET}  {c.CYAN}{shares['submitted']:>6}{c.RESET}                                        │
│  {c.BOLD}SHARES ACCEPTED:{c.RESET}   {c.GREEN}{shares['accepted']:>6}{c.RESET}                                        │
│  {c.BOLD}SHARES REJECTED:{c.RESET}   {c.RED}{shares['rejected']:>6}{c.RESET}                                        │
│                                                                         │
│  {c.BOLD}ACCEPTANCE RATE:{c.RESET}   {acc_color}{acc_rate:>6.1f}%{c.RESET}                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘{c.RESET}
"""
        print(panel)
    
    def _print_footer(self):
        """Print footer with warnings and info"""
        c = Colors
        footer = f"""
{c.DIM}┌─────────────────────────────────────────────────────────────────────────┐
│ {c.YELLOW}⚠{c.RESET}{c.DIM}  EDUCATIONAL PROJECT - NOT FOR PROFITABLE MINING                        │
│    Refresh Rate: 30s │ Press Ctrl+C to terminate                      │
└─────────────────────────────────────────────────────────────────────────┘{c.RESET}
"""
        print(footer)
    
    async def _print_stats_loop(self):
        """Periodically print statistics to console"""
        while self.is_running:
            await asyncio.sleep(30)  # Print every 30 seconds
            self._print_current_stats()
    
    def _print_current_stats(self):
        """Print current mining statistics with sci-fi theme"""
        if not self.stats_history or self.start_time is None:
            return
        
        latest = self.stats_history[-1]
        uptime = datetime.now() - self.start_time
        self.frame_count += 1
        
        # Clear screen for clean update
        self._clear_screen()
        
        # Print all dashboard sections
        self._print_header()
        self._print_system_status(uptime)
        print()
        self._print_workers_table(latest['workers'])
        self._print_statistics_panel(latest)
        self._print_footer()
    
    async def stop(self):
        """Stop the dashboard"""
        self.is_running = False
        logger.info("Dashboard stopped")
    
    def get_stats_summary(self) -> Dict:
        """Get summary of all statistics"""
        if not self.stats_history or self.start_time is None:
            return {}
        
        latest = self.stats_history[-1]
        uptime = datetime.now() - self.start_time
        
        return {
            'uptime_seconds': uptime.total_seconds(),
            'active_workers': sum(1 for w in latest['workers'] if w['connected']),
            'total_workers': len(latest['workers']),
            'total_hashrate': latest['total_hashrate'],
            'shares': latest['shares']
        }
