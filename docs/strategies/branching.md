<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 950">
  <!-- Vertical timeline lines -->
  <line x1="150" y1="50" x2="150" y2="900" stroke="#e0e0e0" stroke-width="2"/>
  <line x1="300" y1="100" x2="300" y2="900" stroke="#e0e0e0" stroke-width="2"/>
  <line x1="450" y1="150" x2="450" y2="500" stroke="#e0e0e0" stroke-width="2"/>
  <line x1="450" y1="550" x2="450" y2="650" stroke="#e0e0e0" stroke-width="2"/>
  <line x1="600" y1="650" x2="600" y2="750" stroke="#e0e0e0" stroke-width="2"/>
  <line x1="450" y1="800" x2="450" y2="900" stroke="#e0e0e0" stroke-width="2"/>
  <line x1="750" y1="700" x2="750" y2="800" stroke="#e0e0e0" stroke-width="2"/>
  
  <!-- Branch labels -->
  <text x="150" y="30" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">main</text>
  <text x="300" y="80" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">staging</text>
  <text x="450" y="130" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">develop/feature-a</text>
  <text x="450" y="530" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">develop/feature-b</text>
  <text x="600" y="630" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">release/v1.0.0</text>
  <text x="450" y="780" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">develop/feature-c</text>
  <text x="750" y="680" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">hotfix/critical-bug</text>
  
  <!-- Initial commit -->
  <circle cx="150" cy="50" r="10" fill="#4CAF50"/>
  
  <!-- Branch to staging -->
  <line x1="150" y1="50" x2="300" y2="100" stroke="#2196F3" stroke-width="2"/>
  <circle cx="300" cy="100" r="10" fill="#2196F3"/>
  
  <!-- Branch to develop feature-a -->
  <line x1="300" y1="100" x2="450" y2="150" stroke="#FF9800" stroke-width="2"/>
  <circle cx="450" cy="150" r="10" fill="#FF9800"/>
  
  <!-- Work on feature-a -->
  <circle cx="450" cy="180" r="10" fill="#FF9800"/>
  <circle cx="450" cy="210" r="10" fill="#FF9800"/>
  <line x1="450" y1="150" x2="450" y2="210" stroke="#FF9800" stroke-width="2"/>
  
  <!-- Merge feature-a back to staging -->
  <line x1="450" y1="210" x2="300" y2="240" stroke="#2196F3" stroke-width="2"/>
  <circle cx="300" cy="240" r="10" fill="#2196F3"/>
  
  <!-- Branch to develop feature-b -->
  <line x1="300" y1="240" x2="450" y2="270" stroke="#FF9800" stroke-width="2"/>
  <circle cx="450" cy="270" r="10" fill="#FF9800"/>
  
  <!-- Work on feature-b -->
  <circle cx="450" cy="300" r="10" fill="#FF9800"/>
  <circle cx="450" cy="330" r="10" fill="#FF9800"/>
  <line x1="450" y1="270" x2="450" y2="330" stroke="#FF9800" stroke-width="2"/>
  
  <!-- Merge feature-b back to staging -->
  <line x1="450" y1="330" x2="300" y2="360" stroke="#2196F3" stroke-width="2"/>
  <circle cx="300" cy="360" r="10" fill="#2196F3"/>
  
  <!-- Branch to release v1.0.0 -->
  <line x1="300" y1="360" x2="600" y2="390" stroke="#9C27B0" stroke-width="2"/>
  <circle cx="600" cy="390" r="10" fill="#9C27B0"/>
  <text x="620" y="395" font-family="Arial" font-size="12">Prepare release</text>
  
  <!-- Merge release to main with tag -->
  <line x1="600" y1="390" x2="150" y2="420" stroke="#4CAF50" stroke-width="2"/>
  <circle cx="150" cy="420" r="10" fill="#4CAF50"/>
  <text x="100" y="420" text-anchor="end" font-family="Arial" font-size="12" font-weight="bold">v1.0.0</text>
  
  <!-- Additional work on staging -->
  <circle cx="300" cy="450" r="10" fill="#2196F3"/>
  <line x1="300" y1="360" x2="300" y2="450" stroke="#2196F3" stroke-width="2"/>
  
  <!-- Branch to develop feature-c -->
  <line x1="300" y1="450" x2="450" y2="480" stroke="#FF9800" stroke-width="2"/>
  <circle cx="450" cy="480" r="10" fill="#FF9800"/>
  
  <!-- Merge feature-c back to staging -->
  <line x1="450" y1="480" x2="300" y2="510" stroke="#2196F3" stroke-width="2"/>
  <circle cx="300" cy="510" r="10" fill="#2196F3"/>
  
  <!-- Create hotfix branch -->
  <line x1="150" y1="420" x2="750" y2="540" stroke="#E91E63" stroke-width="2"/>
  <circle cx="750" cy="540" r="10" fill="#E91E63"/>
  <text x="770" y="545" font-family="Arial" font-size="12">Fix critical issue</text>
  
  <!-- Merge hotfix to main with tag -->
  <line x1="750" y1="540" x2="150" y2="570" stroke="#4CAF50" stroke-width="2"/>
  <circle cx="150" cy="570" r="10" fill="#4CAF50"/>
  <text x="100" y="570" text-anchor="end" font-family="Arial" font-size="12" font-weight="bold">v1.0.1</text>
  
  <!-- Merge hotfix to staging as well -->
  <line x1="750" y1="540" x2="300" y2="600" stroke="#2196F3" stroke-width="2"/>
  <circle cx="300" cy="600" r="10" fill="#2196F3"/>
  
  <!-- Branch to release v1.1.0 -->
  <line x1="300" y1="600" x2="600" y2="630" stroke="#9C27B0" stroke-width="2"/>
  <circle cx="600" cy="630" r="10" fill="#9C27B0"/>
  <text x="620" y="635" font-family="Arial" font-size="12">Prepare next release</text>
  
  <!-- Merge release to main with tag -->
  <line x1="600" y1="630" x2="150" y2="660" stroke="#4CAF50" stroke-width="2"/>
  <circle cx="150" cy="660" r="10" fill="#4CAF50"/>
  <text x="100" y="660" text-anchor="end" font-family="Arial" font-size="12" font-weight="bold">v1.1.0</text>
  
  <!-- Legend -->
  <rect x="50" y="800" width="800" height="100" rx="10" ry="10" fill="#f8f8f8" stroke="#ccc"/>
  <text x="60" y="820" font-family="Arial" font-size="14" font-weight="bold">Legend:</text>
  
  <circle cx="80" cy="840" r="8" fill="#4CAF50"/>
  <text x="100" y="845" font-family="Arial" font-size="14">main branch (Production)</text>
  
  <circle cx="300" cy="840" r="8" fill="#2196F3"/>
  <text x="320" y="845" font-family="Arial" font-size="14">staging branch (Pre-production)</text>
  
  <circle cx="80" cy="870" r="8" fill="#FF9800"/>
  <text x="100" y="875" font-family="Arial" font-size="14">develop/* branches</text>
  
  <circle cx="300" cy="870" r="8" fill="#9C27B0"/>
  <text x="320" y="875" font-family="Arial" font-size="14">release/* branches</text>
  
  <circle cx="550" cy="870" r="8" fill="#E91E63"/>
  <text x="570" y="875" font-family="Arial" font-size="14">hotfix/* branches</text>
</svg>