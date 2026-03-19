                              font=("Segoe UI", 34, "bold"))
        header.pack(pady=(20, 5))

        sub = ctk.CTkLabel(self, text="Track • Analyze • Visualize",
                           font=("Segoe UI", 16))
        sub.pack(pady=(0, 10))

        

        middle_frame = ctk.CTkFrame(self, fg_color="white", height=200)
        middle_frame.pack(fill="x", padx=20)
        middle_frame.pack_propagate(False)

        

        input_frame = ctk.CTkFrame(middle_frame)
        input_frame.pack(side="left", padx=20, pady=20)

        self.category = ctk.CTkEntry(input_frame, placeholder_text="Category")
        self.category.pack(pady=6)

        self.amount = ctk.CTkEntry(input_frame, placeholder_text="Amount")
        self.amount.pack(pady=6)

        self.date = DateEntry(input_frame)
        self.date.pack(pady=6)

        self.note = ctk.CTkEntry(input_frame, placeholder_text="Note")
        self.note.pack(pady=6)

        self.from_date = DateEntry(input_frame)
        self.from_date.pack(pady=4)

        self.to_date = DateEntry(input_frame)
        self.to_date.pack(pady=4)

        ctk.CTkButton(input_frame, text=" Range Total",
                      command=self.range_total).pack(pady=6)

        

        summary = ctk.CTkFrame(middle_frame, width=300)
        summary.pack(side="right", padx=30)

        self.total_label = ctk.CTkLabel(summary,
                                        text="💰 Total Expense\n0",
                                        font=("Segoe UI", 18, "bold"))
        self.total_label.pack(pady=10)

        self.top_label = ctk.CTkLabel(summary,
                                      text="🏆 Top Category\nNone",
                                      font=("Segoe UI", 18, "bold"))
        self.top_label.pack(pady=10)

        self.last_label = ctk.CTkLabel(summary,
                                       text="📅 Last Expense\nNone",
                                       font=("Segoe UI", 18, "bold"))
        self.last_label.pack(pady=10)

        

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="➕ Add",
                      command=self.add).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="✏ Edit",
                      command=self.edit).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="🗑 Delete",
                      command=self.delete).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="🔍 Search",
                      command=self.search).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="Sort ↑",
                      command=lambda: self.sort(False)).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="Sort ↓",
                      command=lambda: self.sort(True)).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="🥧 Pie Chart",
                      command=self.pie_chart).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="📊 Bar Chart",
                      command=self.bar_chart).pack(side="left", padx=5)

        

        style = ttk.Style()
        style.theme_use("default")

        self.tree = ttk.Treeview(self,
                                 columns=("Serial", "Category", "Amount", "Date", "Note"),
                                 show="headings")

        for col in ("Serial", "Category", "Amount", "Date", "Note"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree.pack(in_=table_frame, fill="both", expand=True)

    
